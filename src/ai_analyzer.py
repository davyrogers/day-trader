"""AI analysis module using Ollama for forex news analysis."""
import json
from typing import Dict, Any, List
import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


class OllamaAnalyzer:
    """Handles AI analysis using Ollama models."""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.client = httpx.Client(timeout=300.0)  # 5 minute timeout for large responses
    
    def analyze(self, prompt: str, data: Dict[str, Any]) -> str:
        """Send data to Ollama for analysis."""
        try:
            # Format the data as JSON for the prompt
            data_json = json.dumps(data, indent=2)
            
            # Construct the full prompt
            full_prompt = prompt.replace("{{ JSON.stringify($json.data, null, 2) }}", data_json)
            
            # Make request to Ollama
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except httpx.HTTPError as e:
            console.print(f"[red]HTTP error during analysis with {self.model}: {str(e)}[/red]")
            return f"Error: {str(e)}"
        except Exception as e:
            console.print(f"[red]Error during analysis with {self.model}: {str(e)}[/red]")
            return f"Error: {str(e)}"
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


class ForexAnalysisPipeline:
    """Orchestrates multiple AI analyses of forex news."""
    
    ANALYSIS_PROMPT = """You are reviewing the news for squawk signals related to forex for today, below is the news, you must summarise anything that might cause volitity in the market today, and you should note the time we should be aware of. time is important, data isn't as helpful. 

Here is the news....

{{ JSON.stringify($json.data, null, 2) }}

Your output is sent directly to my mate on discord, so just give a brief, friendly suggestion on what to do today from a forex perspective.  We are normally looking for opportunities to short the EUR/USD so if you see some news that might be worth us looking into for that let us know, but we only really trade the news so if you don't see anything of interest you can just let us know."""
    
    SYNTHESIS_PROMPT = """I have several friends giving me their feedback on the market today, can you summarise for me, here is the info...

{{ JSON.stringify($json.data, null, 2) }}

Send me your thoughts on discord... I'll just pass them directly, so just say what you need to say... don't loose me any money. :) 

make sure you explain any acronyms, and any risk/reward.  I am new to this, you need to spell everything out for me.  base my actions on £100 investment, not leveraged. so if I trade, and we make a short, what would I gain/loose or risk in raw pound notes. give me the odds, in a clear and understandable way. 

We are limited on characters though, as we're sending to discord, so follow BLUF (bottom line up fornt), forget niceities, and just give me what I need to know... shorter the better."""
    
    def __init__(self, ollama_base_url: str, model_20b: str, model_deepseek: str):
        self.ollama_base_url = ollama_base_url
        self.model_20b = model_20b
        self.model_deepseek = model_deepseek
    
    def analyze_news(self, aggregated_data: Dict[str, Any]) -> str:
        """Run multiple AI analyses and synthesize results."""
        
        console.print("\n[bold cyan]Starting AI Analysis[/bold cyan]\n")
        
        # Create analyzers
        analyzers = [
            ("Agent 1 (DeepSeek)", OllamaAnalyzer(self.ollama_base_url, self.model_deepseek)),
            ("Agent 2 (GPT-OSS)", OllamaAnalyzer(self.ollama_base_url, self.model_20b)),
            ("Agent 3 (GPT-OSS)", OllamaAnalyzer(self.ollama_base_url, self.model_20b)),
            ("Agent 4 (GPT-OSS)", OllamaAnalyzer(self.ollama_base_url, self.model_20b)),
        ]
        
        analyses = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running AI analyses...", total=len(analyzers) + 1)
            
            # Run individual analyses
            for name, analyzer in analyzers:
                progress.update(task, description=f"[cyan]{name} analyzing...")
                result = analyzer.analyze(self.ANALYSIS_PROMPT, aggregated_data)
                analyses.append({
                    "agent": name,
                    "output": result
                })
                analyzer.close()
                progress.advance(task)
                console.print(f"[green]✓[/green] {name} complete")
            
            # Synthesize all analyses
            progress.update(task, description="[cyan]Synthesizing results...")
            synthesis_data = {"data": analyses}
            final_analyzer = OllamaAnalyzer(self.ollama_base_url, self.model_20b)
            final_result = final_analyzer.analyze(self.SYNTHESIS_PROMPT, synthesis_data)
            final_analyzer.close()
            progress.advance(task)
            console.print(f"[green]✓[/green] Synthesis complete\n")
        
        return final_result
