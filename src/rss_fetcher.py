"""RSS feed fetcher module for forex news sources."""
import feedparser
import asyncio
import httpx
from typing import List, Dict, Any
from urllib.parse import urlparse
from collections import defaultdict
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import random

console = Console()

# Rate limiting configuration - PER DOMAIN
MAX_CONCURRENT_PER_DOMAIN = 2  # Max simultaneous requests per domain
REQUEST_DELAY_MIN = 0.1  # Minimum delay between requests (seconds)
REQUEST_DELAY_MAX = 0.3  # Maximum delay between requests (seconds)

# Global domain semaphores
_domain_semaphores = defaultdict(lambda: asyncio.Semaphore(MAX_CONCURRENT_PER_DOMAIN))


class RSSFeed:
    """Represents a single RSS feed source."""
    
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.domain = urlparse(url).netloc
    
    async def fetch_async(self) -> List[Dict[str, Any]]:
        """Fetch and parse the RSS feed asynchronously with per-domain rate limiting."""
        # Add random delay to spread out requests
        await asyncio.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))
        
        # Use per-domain semaphore to limit concurrent requests to same domain
        semaphore = _domain_semaphores[self.domain]
        async with semaphore:
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
            # REMOVED - 404 Error: RSSFeed("FXStreet - Forecasts", "https://www.fxstreet.com/rss/forecasts"),
            # REMOVED - 404 Error: RSSFeed("FXStreet - Signals", "https://www.fxstreet.com/rss/signals"),
            
            # DailyForex - Multiple analysis perspectives
            RSSFeed("DailyForex - Forex News", "https://www.dailyforex.com/rss/forexnews.xml"),
            RSSFeed("DailyForex - Technical Analysis", "https://www.dailyforex.com/rss/technicalanalysis.xml"),
            RSSFeed("DailyForex - Fundamental Analysis", "https://www.dailyforex.com/rss/fundamentalanalysis.xml"),
            RSSFeed("DailyForex - Forex Articles", "https://www.dailyforex.com/rss/forexarticles.xml"),
            # REMOVED - 404 Error: RSSFeed("DailyForex - Market News", "https://www.dailyforex.com/rss/marketnews.xml"),
            
            # Investing.com - Major financial news platform
            RSSFeed("InvestingLive", "https://investinglive.com/feed"),
            RSSFeed("Investing.com - Forex News", "https://www.investing.com/rss/news_301.rss"),
            RSSFeed("Investing.com - Economic Indicators", "https://www.investing.com/rss/news_95.rss"),
            RSSFeed("Investing.com - Market Overview", "https://www.investing.com/rss/news_1.rss"),
            RSSFeed("Investing.com - Stock Market", "https://www.investing.com/rss/news_25.rss"),
            # REMOVED - 404 Error: RSSFeed("Investing.com - Commodities", "https://www.investing.com/rss/news_296.rss"),
            RSSFeed("Investing.com - Cryptocurrency", "https://www.investing.com/rss/news_285.rss"),
            
            # ForexLive - Real-time forex commentary
            RSSFeed("ForexLive", "https://www.forexlive.com/feed/news"),
            RSSFeed("ForexLive - Technical Analysis", "https://www.forexlive.com/feed/technicalanalysis"),
            
            # REMOVED - 404 Error: Reuters - Business & Finance
            # REMOVED - 404 Error: RSSFeed("Reuters - Markets", "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"),
            # REMOVED - 404 Error: RSSFeed("Reuters - Business", "https://www.reutersagency.com/feed/?best-sectors=business-finance&post_type=best"),
            
            # Bloomberg via Yahoo Finance
            RSSFeed("Yahoo Finance - Forex", "https://finance.yahoo.com/news/rssindex"),
            
            # FX Empire - Multi-asset coverage (parsing warning but works)
            RSSFeed("FX Empire - Forex", "https://www.fxempire.com/api/v1/en/articles/rss"),
            # REMOVED - 404 Error: RSSFeed("FX Empire - Commodities", "https://www.fxempire.com/api/v1/en/commodities/rss"),
            # REMOVED - 404 Error: RSSFeed("FX Empire - Crypto", "https://www.fxempire.com/api/v1/en/cryptocurrencies/rss"),
            
            # Action Forex
            RSSFeed("Action Forex - News", "https://www.actionforex.com/feed/"),
            
            # REMOVED - 403 Error: ForexFactory
            # REMOVED - 403 Error: RSSFeed("Forex Factory News", "https://www.forexfactory.com/feed.php"),
            
            # REMOVED - 403 Error: MarketWatch
            # REMOVED - 403 Error: RSSFeed("MarketWatch - Currencies", "https://www.marketwatch.com/rss/currencies"),
            # REMOVED - 403 Error: RSSFeed("MarketWatch - Markets", "https://www.marketwatch.com/rss/markets"),
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
            
            # REMOVED - 403 Error: FXCM Insights
            # REMOVED - 403 Error: RSSFeed("FXCM Insights", "https://www.fxcm.com/insights/feed/"),
            
            # REMOVED - 403 Error: Forex.com News
            # REMOVED - 403 Error: RSSFeed("Forex.com - Market News", "https://www.forex.com/en-us/news-and-analysis/feed/"),
            
            # REMOVED - 403 Error: DailyFX
            # REMOVED - 403 Error: RSSFeed("DailyFX", "https://www.dailyfx.com/feeds/market-news"),
            # REMOVED - 403 Error: RSSFeed("DailyFX - Trading News", "https://www.dailyfx.com/feeds/trading-news"),
            
            # Newsquawk
            RSSFeed("Newsquawk", "https://newsquawk.com/blog/feed.rss"),
            
            # REMOVED - 404 Error: OANDA - Market Insights
            # REMOVED - 404 Error: RSSFeed("OANDA - News", "https://www.oanda.com/rw-en/blog/feed/"),
            
            # Benzinga
            RSSFeed("Benzinga - Forex", "https://www.benzinga.com/feed"),
            RSSFeed("Benzinga - Markets", "https://www.benzinga.com/markets/feed"),
            
            # ZeroHedge - Alternative perspective
            RSSFeed("ZeroHedge", "https://feeds.feedburner.com/zerohedge/feed"),
            
            # REMOVED - 404 Error: Kitco - Precious metals
            # REMOVED - 404 Error: RSSFeed("Kitco News", "https://www.kitco.com/rss/KitcoNews.xml"),
            
            # REMOVED - DNS Error: Central Bank News
            # REMOVED - DNS Error: RSSFeed("Central Bank News", "https://www.centralbanksnews.info/feed"),
            
            # REMOVED - 403 Error: ForexNews.com (duplicate of forex.com)
            # REMOVED - 403 Error: RSSFeed("ForexNews.com", "https://www.forex.com/en-us/news-and-analysis/feed/"),
            
            # REMOVED - 404 Error: FXEmpire Technical Analysis
            # REMOVED - 404 Error: RSSFeed("FXEmpire - Technical", "https://www.fxempire.com/api/v1/en/technical-analysis/rss"),
            
            # REMOVED - 403 Error: Trading Economics
            # REMOVED - 403 Error: RSSFeed("Trading Economics", "https://tradingeconomics.com/rss/news"),
            
            # REMOVED - 403 Error: The Street
            # REMOVED - 403 Error: RSSFeed("TheStreet - Markets", "https://www.thestreet.com/feeds/latest-news.xml"),
            
            # Seeking Alpha
            RSSFeed("Seeking Alpha - Forex", "https://seekingalpha.com/feed.xml"),
            RSSFeed("Seeking Alpha - Market News", "https://seekingalpha.com/market_currents.xml"),
            
            # FXDailyReport
            RSSFeed("FXDailyReport", "https://fxdailyreport.com/feed/"),
            
            # REMOVED - 520 Error: LeapRate Forex
            # REMOVED - 520 Error: RSSFeed("LeapRate - Forex", "https://www.leaprate.com/feed/"),
            
            # Finance Magnates
            RSSFeed("Finance Magnates - Forex", "https://www.financemagnates.com/feed/"),
            
            # REMOVED - 404 Error: TipRanks Economics
            # REMOVED - 404 Error: RSSFeed("TipRanks - Economic Calendar", "https://www.tipranks.com/api/feed/"),
            
            # FXOpen Blog
            RSSFeed("FXOpen Blog", "https://blog.fxopen.com/feed/"),
            
            # REMOVED - 404 Error: Admirals
            # REMOVED - 404 Error: RSSFeed("Admirals - News", "https://admiralmarkets.com/news/rss"),
            
            # IC Markets
            RSSFeed("IC Markets - News", "https://www.icmarkets.com/blog/feed/"),
            
            # REMOVED - 404 Error: Pepperstone
            # REMOVED - 404 Error: RSSFeed("Pepperstone - News", "https://www.pepperstone.com/en/blog/feed"),
            
            # REMOVED - Parsing Error: XM Research
            # REMOVED - Parsing Error: RSSFeed("XM - Research", "https://www.xm.com/research/feed"),
            
            # eToro Market Updates
            RSSFeed("eToro - Market Analysis", "https://www.etoro.com/news-and-analysis/feed/"),
            
            # REMOVED - 403 Error: Plus500 News
            # REMOVED - 403 Error: RSSFeed("Plus500 - Insights", "https://www.plus500.com/en-US/NewsAndMarketInsights/RSS"),
            
            # REMOVED - 404 Error: IG Market News
            # REMOVED - 404 Error: RSSFeed("IG - Daily Market News", "https://www.ig.com/uk/news-and-trade-ideas/rss"),
            
            # REMOVED - 404 Error: CMC Markets
            # REMOVED - 404 Error: RSSFeed("CMC Markets - News", "https://www.cmcmarkets.com/en/rss/news-and-analysis"),
            
            # REMOVED - 404 Error: Saxo Bank
            # REMOVED - 404 Error: RSSFeed("Saxo Bank - Research", "https://www.home.saxo/en-gb/insights/rss"),
            
            # REMOVED - 404 Error: Interactive Brokers
            # REMOVED - 404 Error: RSSFeed("IBKR - Traders Insight", "https://www.interactivebrokers.com/rss/newsroom.xml"),
            
            # REMOVED - 404 Error: Myfxbook
            # REMOVED - 404 Error: RSSFeed("Myfxbook - Market Outlook", "https://www.myfxbook.com/community/feed"),
            
            # REMOVED - 404 Error: Dukascopy
            # REMOVED - 404 Error: RSSFeed("Dukascopy - Analytics", "https://www.dukascopy.com/swiss/english/marketwatch/news/feed/"),
            
            # REMOVED - 404 Error: FXStreet Additional Feeds
            # REMOVED - 404 Error: RSSFeed("FXStreet - Market Movers", "https://www.fxstreet.com/rss/market-movers"),
            # REMOVED - 404 Error: RSSFeed("FXStreet - Cryptocurrencies", "https://www.fxstreet.com/rss/cryptocurrencies"),
            
            # REMOVED - 404 Error: Economic Calendar Sources
            # REMOVED - 404 Error: RSSFeed("Econoday", "https://www.econoday.com/rss.aspx"),
            
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
        """Internal async method to fetch all feeds concurrently with per-domain rate limiting."""
        all_entries = []
        results = {}
        
        # Count unique domains
        domains = set(feed.domain for feed in self.feeds)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Fetching RSS feeds concurrently...", total=len(self.feeds))
            
            # Create tasks for all feeds with per-domain rate limiting
            console.print(f"[dim]Fetching {len(self.feeds)} feeds from {len(domains)} domains (max {MAX_CONCURRENT_PER_DOMAIN} per domain)...[/dim]")
            feed_tasks = [feed.fetch_async() for feed in self.feeds]
            
            # Fetch all feeds concurrently with per-domain rate limiting
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
