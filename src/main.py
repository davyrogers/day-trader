"""Main workflow orchestrator for the forex news analysis system."""
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from config import settings
from rss_fetcher import RSSFeedAggregator
from ai_analyzer import ForexAnalysisPipeline
from discord_sender import DiscordSender

console = Console()


class SquawkWorkflow:
    """Main workflow orchestrator."""
    
    def __init__(self):
        self.rss_aggregator = RSSFeedAggregator()
        self.ai_pipeline = ForexAnalysisPipeline(
            ollama_base_url=settings.ollama_base_url,
            model_20b=settings.ollama_model_20b,
            model_deepseek=settings.ollama_model_deepseek
        )
        self.discord_sender = DiscordSender(
            webhook_url=settings.discord_webhook_url
        )
    
    def run(self):
        """Execute the complete workflow."""
        start_time = time.time()
        
        # Display banner
        self._display_banner()
        
        try:
            # Step 1: Fetch RSS feeds
            console.print("[bold cyan]Step 1: Fetching RSS Feeds[/bold cyan]")
            aggregated_data = self.rss_aggregator.fetch_all()
            
            if not aggregated_data.get("data"):
                console.print("[red]No data fetched. Exiting.[/red]")
                return
            
            # Step 2: AI Analysis
            console.print("[bold cyan]Step 2: AI Analysis[/bold cyan]")
            analysis_result = self.ai_pipeline.analyze_news(aggregated_data)
            
            # Step 3: Send to Discord
            console.print("[bold cyan]Step 3: Sending to Discord[/bold cyan]\n")
            self.discord_sender.send_message(analysis_result)
            
            # Summary
            elapsed_time = time.time() - start_time
            self._display_summary(elapsed_time, len(aggregated_data.get("data", [])))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Workflow interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error during workflow execution: {str(e)}[/red]")
        finally:
            self.discord_sender.close()
    
    def _display_banner(self):
        """Display the application banner."""
        banner = Text()
        banner.append("╔═══════════════════════════════════════╗\n", style="bold cyan")
        banner.append("║   ", style="bold cyan")
        banner.append("FOREX NEWS SQUAWK ANALYZER", style="bold yellow")
        banner.append("    ║\n", style="bold cyan")
        banner.append("╚═══════════════════════════════════════╝", style="bold cyan")
        
        console.print(Panel(banner, border_style="cyan"))
        console.print(f"[dim]Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
    
    def _display_summary(self, elapsed_time: float, article_count: int):
        """Display workflow summary."""
        summary = Text()
        summary.append("Workflow Complete!\n\n", style="bold green")
        summary.append(f"• Articles analyzed: {article_count}\n")
        summary.append(f"• Time elapsed: {elapsed_time:.2f} seconds\n")
        summary.append(f"• Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        console.print(Panel(summary, title="Summary", border_style="green"))


def main():
    """Main entry point."""
    workflow = SquawkWorkflow()
    
    if settings.run_once:
        console.print("[dim]Running workflow once...[/dim]\n")
        workflow.run()
    else:
        console.print(f"[dim]Scheduling workflow to run every {settings.schedule_interval_hours} hour(s)[/dim]")
        console.print("[dim]Press Ctrl+C to stop[/dim]\n")
        
        import schedule
        schedule.every(settings.schedule_interval_hours).hours.do(workflow.run)
        
        # Run immediately
        workflow.run()
        
        # Then run on schedule
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__":
    main()
