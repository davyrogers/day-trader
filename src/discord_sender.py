"""Discord integration module for sending analysis results."""
import httpx
from rich.console import Console

console = Console()


class DiscordSender:
    """Handles sending messages to Discord via webhook."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.client = httpx.Client(timeout=30.0)
    
    def send_message(self, content: str) -> bool:
        """Send a message to Discord."""
        if not self.webhook_url:
            console.print("[yellow]Warning: No Discord webhook URL configured. Skipping Discord notification.[/yellow]")
            console.print("\n[bold]Analysis Result:[/bold]")
            console.print(f"{content}\n")
            return False
        
        try:
            # Discord has a 2000 character limit
            if len(content) > 2000:
                console.print("[yellow]Warning: Message exceeds Discord's 2000 character limit. Truncating...[/yellow]")
                content = content[:1997] + "..."
            
            response = self.client.post(
                self.webhook_url,
                json={"content": content}
            )
            response.raise_for_status()
            
            console.print("[green]✓[/green] Message sent to Discord successfully")
            return True
            
        except httpx.HTTPError as e:
            console.print(f"[red]Error sending to Discord: {str(e)}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Unexpected error sending to Discord: {str(e)}[/red]")
            return False
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
