"""RSS feed fetcher module for forex news sources."""
import feedparser
import asyncio
import httpx
from typing import List, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class RSSFeed:
    """Represents a single RSS feed source."""
    
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    
    async def fetch_async(self) -> List[Dict[str, Any]]:
        """Fetch and parse the RSS feed asynchronously."""
        try:
            # Fetch the feed content asynchronously
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.url)
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
            
            # DailyForex - Multiple analysis perspectives
            RSSFeed("DailyForex - Forex News", "https://www.dailyforex.com/rss/forexnews.xml"),
            RSSFeed("DailyForex - Technical Analysis", "https://www.dailyforex.com/rss/technicalanalysis.xml"),
            RSSFeed("DailyForex - Fundamental Analysis", "https://www.dailyforex.com/rss/fundamentalanalysis.xml"),
            RSSFeed("DailyForex - Forex Articles", "https://www.dailyforex.com/rss/forexarticles.xml"),
            
            # Investing.com - Major financial news platform
            RSSFeed("InvestingLive", "https://investinglive.com/feed"),
            RSSFeed("Investing.com - Forex News", "https://www.investing.com/rss/news_301.rss"),
            RSSFeed("Investing.com - Economic Indicators", "https://www.investing.com/rss/news_95.rss"),
            RSSFeed("Investing.com - Market Overview", "https://www.investing.com/rss/news_1.rss"),
            
            # ForexLive - Real-time forex commentary
            RSSFeed("ForexLive", "https://www.forexlive.com/feed/news"),
            
            # Reuters - Business & Finance
            RSSFeed("Reuters - Markets", "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"),
            
            # Bloomberg via Yahoo Finance
            RSSFeed("Yahoo Finance - Forex", "https://finance.yahoo.com/news/rssindex"),
            
            # FX Empire - Multi-asset coverage
            RSSFeed("FX Empire - Forex", "https://www.fxempire.com/api/v1/en/articles/rss"),
            
            # Action Forex
            RSSFeed("Action Forex - News", "https://www.actionforex.com/feed/"),
            
            # ForexFactory (if available)
            RSSFeed("Forex Factory News", "https://www.forexfactory.com/feed.php"),
            
            # MarketWatch
            RSSFeed("MarketWatch - Currencies", "https://www.marketwatch.com/rss/currencies"),
            RSSFeed("MarketWatch - Markets", "https://www.marketwatch.com/rss/markets"),
            
            # Financial Times
            RSSFeed("FT - Markets", "https://www.ft.com/markets?format=rss"),
            RSSFeed("FT - Currencies", "https://www.ft.com/currencies?format=rss"),
            
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
            
            # Newsquawk
            RSSFeed("Newsquawk", "https://newsquawk.com/blog/feed.rss"),
            
            # OANDA - Market Insights
            RSSFeed("OANDA - News", "https://www.oanda.com/rw-en/blog/feed/"),
            
            # Benzinga Forex
            RSSFeed("Benzinga - Forex", "https://www.benzinga.com/feed"),
            
            # ZeroHedge - Alternative perspective
            RSSFeed("ZeroHedge", "https://feeds.feedburner.com/zerohedge/feed"),
            
            # Kitco - Precious metals (affects forex)
            RSSFeed("Kitco News", "https://www.kitco.com/rss/KitcoNews.xml"),
            
            # Central Bank News
            RSSFeed("Central Bank News", "https://www.centralbanksnews.info/feed"),
            
            # ForexNews.com
            RSSFeed("ForexNews.com", "https://www.forex.com/en-us/news-and-analysis/feed/"),
        ]
    
    def fetch_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all RSS feeds concurrently and return aggregated data."""
        return asyncio.run(self._fetch_all_async())
    
    async def _fetch_all_async(self) -> Dict[str, List[Dict[str, Any]]]:
        """Internal async method to fetch all feeds concurrently."""
        all_entries = []
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Fetching RSS feeds concurrently...", total=len(self.feeds))
            
            # Create tasks for all feeds
            console.print("[dim]Fetching 8 feeds in parallel...[/dim]")
            feed_tasks = [feed.fetch_async() for feed in self.feeds]
            
            # Fetch all feeds concurrently
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
