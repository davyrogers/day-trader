"""Market data fetcher for real-time forex prices."""
import asyncio
import httpx
from typing import Dict, Any, Optional
from rich.console import Console
from datetime import datetime

console = Console()


class MarketDataFetcher:
    """Fetches real-time market data for forex pairs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize market data fetcher.
        
        Args:
            api_key: Optional API key for premium data sources
        """
        self.api_key = api_key
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = 60  # Cache for 60 seconds
        
    async def get_forex_data_async(self, symbol: str = "EUR/USD") -> Dict[str, Any]:
        """
        Fetch real-time forex data for a given symbol.
        
        Args:
            symbol: Forex pair symbol (default: EUR/USD)
            
        Returns:
            Dictionary containing market data
        """
        # Check cache first
        if symbol in self.cache:
            cached_data = self.cache[symbol]
            if (datetime.now() - cached_data['timestamp']).seconds < self.cache_duration:
                console.print(f"[dim]Using cached market data for {symbol}[/dim]")
                return cached_data['data']
        
        try:
            # Try multiple free data sources in order
            data = await self._fetch_from_exchangerate_api(symbol)
            if not data:
                data = await self._fetch_from_frankfurter(symbol)
            if not data:
                data = await self._fetch_from_fixer(symbol)
            
            if data:
                # Cache the result
                self.cache[symbol] = {
                    'data': data,
                    'timestamp': datetime.now()
                }
                return data
            else:
                console.print(f"[yellow]Warning: Could not fetch market data for {symbol}[/yellow]")
                return self._get_fallback_data(symbol)
                
        except Exception as e:
            console.print(f"[red]Error fetching market data: {str(e)}[/red]")
            return self._get_fallback_data(symbol)
    
    async def _fetch_from_exchangerate_api(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch from exchangerate-api.com (free, no key required)."""
        try:
            base, quote = self._parse_symbol(symbol)
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"https://open.er-api.com/v6/latest/{base}"
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('result') == 'success' and quote in data.get('rates', {}):
                    rate = data['rates'][quote]
                    return {
                        'symbol': symbol,
                        'price': rate,
                        'bid': rate * 0.9999,  # Estimate spread
                        'ask': rate * 1.0001,
                        'source': 'exchangerate-api.com',
                        'timestamp': data.get('time_last_update_utc', 'N/A'),
                        'note': 'Estimated bid/ask spread based on typical forex spreads'
                    }
        except Exception as e:
            console.print(f"[dim]exchangerate-api failed: {str(e)}[/dim]")
            return None
    
    async def _fetch_from_frankfurter(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch from frankfurter.app (free ECB data, no key required)."""
        try:
            base, quote = self._parse_symbol(symbol)
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"https://api.frankfurter.app/latest?from={base}&to={quote}"
                )
                response.raise_for_status()
                data = response.json()
                
                if quote in data.get('rates', {}):
                    rate = data['rates'][quote]
                    return {
                        'symbol': symbol,
                        'price': rate,
                        'bid': rate * 0.9999,
                        'ask': rate * 1.0001,
                        'source': 'frankfurter.app (ECB)',
                        'timestamp': data.get('date', 'N/A'),
                        'note': 'Estimated bid/ask spread based on typical forex spreads'
                    }
        except Exception as e:
            console.print(f"[dim]frankfurter.app failed: {str(e)}[/dim]")
            return None
    
    async def _fetch_from_fixer(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch from fixer.io (requires free API key if available)."""
        if not self.api_key:
            return None
            
        try:
            base, quote = self._parse_symbol(symbol)
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"http://data.fixer.io/api/latest?access_key={self.api_key}&base={base}&symbols={quote}"
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('success') and quote in data.get('rates', {}):
                    rate = data['rates'][quote]
                    return {
                        'symbol': symbol,
                        'price': rate,
                        'bid': rate * 0.9999,
                        'ask': rate * 1.0001,
                        'source': 'fixer.io',
                        'timestamp': data.get('date', 'N/A'),
                        'note': 'Estimated bid/ask spread based on typical forex spreads'
                    }
        except Exception as e:
            console.print(f"[dim]fixer.io failed: {str(e)}[/dim]")
            return None
    
    def _parse_symbol(self, symbol: str) -> tuple:
        """Parse forex symbol into base and quote currencies."""
        symbol = symbol.replace('/', '').replace(' ', '')
        if len(symbol) == 6:
            return symbol[:3], symbol[3:]
        else:
            # Default to EUR/USD
            return 'EUR', 'USD'
    
    def _get_fallback_data(self, symbol: str) -> Dict[str, Any]:
        """Return fallback data when APIs fail."""
        console.print(f"[yellow]Using fallback market data for {symbol}[/yellow]")
        return {
            'symbol': symbol,
            'price': 'N/A',
            'bid': 'N/A',
            'ask': 'N/A',
            'source': 'Fallback (APIs unavailable)',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'note': 'CRITICAL: Real market data unavailable. Do not trade based on this information.'
        }
    
    def format_market_data(self, data: Dict[str, Any]) -> str:
        """Format market data for inclusion in prompts."""
        if data['price'] == 'N/A':
            return f"""
MARKET DATA STATUS: UNAVAILABLE
Source: {data['source']}
Note: {data['note']}

⚠️ CRITICAL: Real-time market data could not be retrieved.
Management should NOT make specific price-based recommendations without current market data.
Focus on timing and directional bias only.
"""
        
        return f"""
━━━━ REAL-TIME MARKET DATA ━━━━
Symbol: {data['symbol']}
Current Price: {data['price']:.5f}
Bid: {data['bid']:.5f}
Ask: {data['ask']:.5f}
Spread: {(data['ask'] - data['bid']):.5f} ({((data['ask'] - data['bid']) / data['price'] * 10000):.1f} pips)
Source: {data['source']}
Updated: {data['timestamp']}
{data.get('note', '')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def get_forex_data(self, symbol: str = "EUR/USD") -> Dict[str, Any]:
        """Synchronous wrapper for get_forex_data_async."""
        return asyncio.run(self.get_forex_data_async(symbol))


def extract_instrument_from_news(aggregated_data: Dict[str, Any]) -> str:
    """
    Extract the trading instrument from news data.
    
    Args:
        aggregated_data: The aggregated news data
        
    Returns:
        Trading instrument symbol (e.g., "EUR/USD")
    """
    # For now, default to EUR/USD as mentioned in analyst prompts
    # This could be enhanced to parse news content and identify the instrument
    
    # Check if there's an explicit instrument field
    if 'instrument' in aggregated_data:
        return aggregated_data['instrument']
    
    # Parse news content for forex pairs
    news_text = str(aggregated_data).upper()
    
    common_pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CHF', 'USD/CAD']
    for pair in common_pairs:
        if pair in news_text or pair.replace('/', '') in news_text:
            console.print(f"[cyan]Detected forex pair from news: {pair}[/cyan]")
            return pair
    
    # Default to EUR/USD
    console.print("[dim]No specific forex pair detected, defaulting to EUR/USD[/dim]")
    return "EUR/USD"


# Example usage
if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    data = fetcher.get_forex_data("EUR/USD")
    print(fetcher.format_market_data(data))
