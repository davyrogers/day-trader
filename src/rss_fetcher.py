"""RSS feed fetcher module for forex news sources."""
import feedparser
from typing import List, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class RSSFeed:
    """Represents a single RSS feed source."""
    
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch and parse the RSS feed."""
        try:
            feed = feedparser.parse(self.url)
            
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
        except Exception as e:
            console.print(f"[red]Error fetching {self.name}: {str(e)}[/red]")
            return []


class RSSFeedAggregator:
    """Aggregates multiple RSS feeds."""
    
    def __init__(self):
        self.feeds = [
            RSSFeed("FXStreet - News", "https://www.fxstreet.com/rss/news"),
            RSSFeed("FXStreet - Analysis", "https://www.fxstreet.com/rss/analysis"),
            RSSFeed("InvestingLive", "https://investinglive.com/feed"),
            RSSFeed("DailyForex - Forex News", "https://www.dailyforex.com/rss/forexnews.xml"),
            RSSFeed("DailyForex - Technical Analysis", "https://www.dailyforex.com/rss/technicalanalysis.xml"),
            RSSFeed("DailyForex - Fundamental Analysis", "https://www.dailyforex.com/rss/fundamentalanalysis.xml"),
            RSSFeed("DailyForex - Forex Articles", "https://www.dailyforex.com/rss/forexarticles.xml"),
            RSSFeed("Newsquawk", "https://newsquawk.com/blog/feed.rss"),
        ]
    
    def fetch_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all RSS feeds and return aggregated data."""
        all_entries = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Fetching RSS feeds...", total=len(self.feeds))
            
            for feed in self.feeds:
                progress.update(task, description=f"[cyan]Fetching {feed.name}...")
                entries = feed.fetch()
                all_entries.extend(entries)
                progress.advance(task)
                console.print(f"[green]✓[/green] {feed.name}: {len(entries)} articles")
        
        console.print(f"\n[bold green]Total articles fetched: {len(all_entries)}[/bold green]\n")
        
        return {"data": all_entries}
