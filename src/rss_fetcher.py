"""RSS feed fetcher module for forex news sources."""
import feedparser
import asyncio
import httpx
from typing import List, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import random

console = Console()

# Rate limiting configuration
MAX_CONCURRENT_REQUESTS = 10  # Max simultaneous requests
REQUEST_DELAY_MIN = 0.1  # Minimum delay between requests (seconds)
REQUEST_DELAY_MAX = 0.3  # Maximum delay between requests (seconds)


class RSSFeed:
    """Represents a single RSS feed source."""
    
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    
    async def fetch_async(self, semaphore: asyncio.Semaphore = None) -> List[Dict[str, Any]]:
        """Fetch and parse the RSS feed asynchronously with rate limiting."""
        # Add random delay to spread out requests
        await asyncio.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))
        
        # Use semaphore if provided to limit concurrent requests
        if semaphore:
            async with semaphore:
                return await self._do_fetch()
        else:
            return await self._do_fetch()
    
    async def _do_fetch(self) -> List[Dict[str, Any]]:
        """Internal method to perform the actual fetch."""
        try:
            # Fetch the feed content asynchronously with custom headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            }
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(self.url, headers=headers)
                response.raise_for_status()
                feed_content = response.text
            
            # Parse with feedparser (synchronous but fast)
            feed = feedparser.parse(feed_content)
            
            if feed.bozo:  # Check for parsing errors
                console.print(f"[yellow]Warning parsing {self.name}: {feed.bozo_exception}[/yellow]")
            
            entries = []
            for entry in feed.entries:
                entries.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'pubDate': entry.get('published', ''),
                    'content': entry.get('summary', entry.get('content', [{}])[0].get('value', '')),
                    'contentSnippet': entry.get('summary', ''),
                    'guid': entry.get('id', entry.get('link', '')),
                    'isoDate': entry.get('published_parsed', ''),
                })
            
            return entries
        except httpx.HTTPError as e:
            console.print(f"[red]HTTP error fetching {self.name}: {str(e)}[/red]")
            return []
        except Exception as e:
            console.print(f"[red]Error fetching {self.name}: {str(e)}[/red]")
            return []
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Synchronous wrapper for fetch_async."""
        return asyncio.run(self.fetch_async())


class RSSFeedAggregator:
    """Aggregates multiple RSS feeds."""
    
    def __init__(self):
        self.feeds = [
            # FXStreet - Comprehensive forex coverage
            RSSFeed("FXStreet - News", "https://www.fxstreet.com/rss/news"),
            RSSFeed("FXStreet - Analysis", "https://www.fxstreet.com/rss/analysis"),
            RSSFeed("FXStreet - Forecasts", "https://www.fxstreet.com/rss/forecasts"),
            RSSFeed("FXStreet - Signals", "https://www.fxstreet.com/rss/signals"),
            
            # DailyForex - Multiple analysis perspectives
            RSSFeed("DailyForex - Forex News", "https://www.dailyforex.com/rss/forexnews.xml"),
            RSSFeed("DailyForex - Technical Analysis", "https://www.dailyforex.com/rss/technicalanalysis.xml"),
            RSSFeed("DailyForex - Fundamental Analysis", "https://www.dailyforex.com/rss/fundamentalanalysis.xml"),
            RSSFeed("DailyForex - Forex Articles", "https://www.dailyforex.com/rss/forexarticles.xml"),
            RSSFeed("DailyForex - Market News", "https://www.dailyforex.com/rss/marketnews.xml"),
            
            # Investing.com - Major financial news platform
            RSSFeed("InvestingLive", "https://investinglive.com/feed"),
            RSSFeed("Investing.com - Forex News", "https://www.investing.com/rss/news_301.rss"),
            RSSFeed("Investing.com - Economic Indicators", "https://www.investing.com/rss/news_95.rss"),
            RSSFeed("Investing.com - Market Overview", "https://www.investing.com/rss/news_1.rss"),
            RSSFeed("Investing.com - Stock Market", "https://www.investing.com/rss/news_25.rss"),
            RSSFeed("Investing.com - Commodities", "https://www.investing.com/rss/news_296.rss"),
            RSSFeed("Investing.com - Cryptocurrency", "https://www.investing.com/rss/news_285.rss"),
            
            # ForexLive - Real-time forex commentary
            RSSFeed("ForexLive", "https://www.forexlive.com/feed/news"),
            RSSFeed("ForexLive - Technical Analysis", "https://www.forexlive.com/feed/technicalanalysis"),
            
            # Reuters - Business & Finance
            RSSFeed("Reuters - Markets", "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"),
            RSSFeed("Reuters - Business", "https://www.reutersagency.com/feed/?best-sectors=business-finance&post_type=best"),
            
            # Bloomberg via Yahoo Finance
            RSSFeed("Yahoo Finance - Forex", "https://finance.yahoo.com/news/rssindex"),
            
            # FX Empire - Multi-asset coverage
            RSSFeed("FX Empire - Forex", "https://www.fxempire.com/api/v1/en/articles/rss"),
            RSSFeed("FX Empire - Commodities", "https://www.fxempire.com/api/v1/en/commodities/rss"),
            RSSFeed("FX Empire - Crypto", "https://www.fxempire.com/api/v1/en/cryptocurrencies/rss"),
            
            # Action Forex
            RSSFeed("Action Forex - News", "https://www.actionforex.com/feed/"),
            
            # ForexFactory (if available)
            RSSFeed("Forex Factory News", "https://www.forexfactory.com/feed.php"),
            
            # MarketWatch
            RSSFeed("MarketWatch - Currencies", "https://www.marketwatch.com/rss/currencies"),
            RSSFeed("MarketWatch - Markets", "https://www.marketwatch.com/rss/markets"),
            RSSFeed("MarketWatch - Top Stories", "https://www.marketwatch.com/rss/topstories"),
            RSSFeed("MarketWatch - Breaking News", "https://www.marketwatch.com/rss/realtimeheadlines"),
            
            # Financial Times
            RSSFeed("FT - Markets", "https://www.ft.com/markets?format=rss"),
            RSSFeed("FT - Currencies", "https://www.ft.com/currencies?format=rss"),
            RSSFeed("FT - Commodities", "https://www.ft.com/commodities?format=rss"),
            RSSFeed("FT - World Economy", "https://www.ft.com/world-economy?format=rss"),
            
            # TradingView Ideas
            RSSFeed("TradingView - Forex Ideas", "https://www.tradingview.com/feed/"),
            
            # ForexCrunch
            RSSFeed("ForexCrunch", "https://www.forexcrunch.com/feed/"),
            
            # FXCM Insights
            RSSFeed("FXCM Insights", "https://www.fxcm.com/insights/feed/"),
            
            # Forex.com News
            RSSFeed("Forex.com - Market News", "https://www.forex.com/en-us/news-and-analysis/feed/"),
            
            # DailyFX
            RSSFeed("DailyFX", "https://www.dailyfx.com/feeds/market-news"),
            RSSFeed("DailyFX - Trading News", "https://www.dailyfx.com/feeds/trading-news"),
            
            # Newsquawk
            RSSFeed("Newsquawk", "https://newsquawk.com/blog/feed.rss"),
            
            # OANDA - Market Insights
            RSSFeed("OANDA - News", "https://www.oanda.com/rw-en/blog/feed/"),
            
            # Benzinga
            RSSFeed("Benzinga - Forex", "https://www.benzinga.com/feed"),
            RSSFeed("Benzinga - Markets", "https://www.benzinga.com/markets/feed"),
            
            # ZeroHedge - Alternative perspective
            RSSFeed("ZeroHedge", "https://feeds.feedburner.com/zerohedge/feed"),
            
            # Kitco - Precious metals (affects forex)
            RSSFeed("Kitco News", "https://www.kitco.com/rss/KitcoNews.xml"),
            
            # Central Bank News
            RSSFeed("Central Bank News", "https://www.centralbanksnews.info/feed"),
            
            # ForexNews.com
            RSSFeed("ForexNews.com", "https://www.forex.com/en-us/news-and-analysis/feed/"),
            
            # FXEmpire Technical Analysis
            RSSFeed("FXEmpire - Technical", "https://www.fxempire.com/api/v1/en/technical-analysis/rss"),
            
            # Trading Economics
            RSSFeed("Trading Economics", "https://tradingeconomics.com/rss/news"),
            
            # The Street
            RSSFeed("TheStreet - Markets", "https://www.thestreet.com/feeds/latest-news.xml"),
            
            # Seeking Alpha
            RSSFeed("Seeking Alpha - Forex", "https://seekingalpha.com/feed.xml"),
            RSSFeed("Seeking Alpha - Market News", "https://seekingalpha.com/market_currents.xml"),
            
            # FXDailyReport
            RSSFeed("FXDailyReport", "https://fxdailyreport.com/feed/"),
            
            # LeapRate Forex
            RSSFeed("LeapRate - Forex", "https://www.leaprate.com/feed/"),
            
            # Finance Magnates
            RSSFeed("Finance Magnates - Forex", "https://www.financemagnates.com/feed/"),
            
            # TipRanks Economics
            RSSFeed("TipRanks - Economic Calendar", "https://www.tipranks.com/api/feed/"),
            
            # FXOpen Blog
            RSSFeed("FXOpen Blog", "https://blog.fxopen.com/feed/"),
            
            # Admirals (formerly Admiral Markets)
            RSSFeed("Admirals - News", "https://admiralmarkets.com/news/rss"),
            
            # IC Markets
            RSSFeed("IC Markets - News", "https://www.icmarkets.com/blog/feed/"),
            
            # Pepperstone
            RSSFeed("Pepperstone - News", "https://www.pepperstone.com/en/blog/feed"),
            
            # XM Research
            RSSFeed("XM - Research", "https://www.xm.com/research/feed"),
            
            # eToro Market Updates
            RSSFeed("eToro - Market Analysis", "https://www.etoro.com/news-and-analysis/feed/"),
            
            # Plus500 News
            RSSFeed("Plus500 - Insights", "https://www.plus500.com/en-US/NewsAndMarketInsights/RSS"),
            
            # IG Market News
            RSSFeed("IG - Daily Market News", "https://www.ig.com/uk/news-and-trade-ideas/rss"),
            
            # CMC Markets
            RSSFeed("CMC Markets - News", "https://www.cmcmarkets.com/en/rss/news-and-analysis"),
            
            # Saxo Bank
            RSSFeed("Saxo Bank - Research", "https://www.home.saxo/en-gb/insights/rss"),
            
            # Interactive Brokers
            RSSFeed("IBKR - Traders Insight", "https://www.interactivebrokers.com/rss/newsroom.xml"),
            
            # Myfxbook
            RSSFeed("Myfxbook - Market Outlook", "https://www.myfxbook.com/community/feed"),
            
            # Dukascopy
            RSSFeed("Dukascopy - Analytics", "https://www.dukascopy.com/swiss/english/marketwatch/news/feed/"),
            
            # FXStreet Additional Feeds
            RSSFeed("FXStreet - Market Movers", "https://www.fxstreet.com/rss/market-movers"),
            RSSFeed("FXStreet - Cryptocurrencies", "https://www.fxstreet.com/rss/cryptocurrencies"),
            
            # Economic Calendar Sources
            RSSFeed("Econoday", "https://www.econoday.com/rss.aspx"),
            
            # Mish Talk (Mike Shedlock)
            RSSFeed("Mish Talk - Global Economics", "https://mishtalk.com/feed"),
            
            # Wolf Street
            RSSFeed("Wolf Street - Economy", "https://wolfstreet.com/feed/"),
            
            # Calculated Risk (Bill McBride)
            RSSFeed("Calculated Risk - Economy", "https://www.calculatedriskblog.com/feeds/posts/default"),
            
            # Credit Writedowns
            RSSFeed("Credit Writedowns", "https://www.creditwritedowns.com/feed"),
        ]
    
    def fetch_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all RSS feeds concurrently and return aggregated data."""
        return asyncio.run(self._fetch_all_async())
    
    async def _fetch_all_async(self) -> Dict[str, List[Dict[str, Any]]]:
        """Internal async method to fetch all feeds concurrently with rate limiting."""
        all_entries = []
        results = {}
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Fetching RSS feeds concurrently...", total=len(self.feeds))
            
            # Create tasks for all feeds with rate limiting
            console.print(f"[dim]Fetching {len(self.feeds)} feeds with rate limiting (max {MAX_CONCURRENT_REQUESTS} concurrent)...[/dim]")
            feed_tasks = [feed.fetch_async(semaphore) for feed in self.feeds]
            
            # Fetch all feeds concurrently with rate limiting
            feed_results = await asyncio.gather(*feed_tasks, return_exceptions=True)
            
            # Process results
            for feed, entries in zip(self.feeds, feed_results):
                if isinstance(entries, Exception):
                    console.print(f"[red]✗[/red] {feed.name}: Failed - {str(entries)}")
                    entries = []
                else:
                    all_entries.extend(entries)
                    console.print(f"[green]✓[/green] {feed.name}: {len(entries)} articles")
                
                progress.advance(task)
        
        console.print(f"\n[bold green]Total articles fetched: {len(all_entries)}[/bold green]\n")
        
        return {"data": all_entries}
