"""AI analysis module using Ollama for forex news analysis."""
import json
import asyncio
from typing import Dict, Any, List
import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


class OllamaAnalyzer:
    """Handles AI analysis using Ollama models."""
    
    def __init__(self, base_url: str, model: str, temperature: float = 0.8):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
    
    async def analyze_async(self, prompt: str, data: Dict[str, Any]) -> str:
        """Send data to Ollama for analysis asynchronously."""
        try:
            # Format the data as JSON for the prompt
            data_json = json.dumps(data, indent=2)
            
            # Construct the full prompt
            full_prompt = prompt.replace("{{ JSON.stringify($json.data, null, 2) }}", data_json)
            
            # Make async request to Ollama with temperature
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False,
                        "keep_alive": 0,  # Unload model after each request to avoid context mixing
                        "options": {
                            "temperature": self.temperature
                        }
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
    
    def analyze(self, prompt: str, data: Dict[str, Any]) -> str:
        """Synchronous wrapper for analyze_async."""
        return asyncio.run(self.analyze_async(prompt, data))


class ForexAnalysisPipeline:
    """Orchestrates multiple AI analyses of forex news."""
    
    ANALYSIS_PROMPT = """You are reviewing the news for squawk signals related to forex for today, below is the news, you must summarise anything that might cause volitity in the market today, and you should note the time we should be aware of. time is important, data isn't as helpful. 

Here is the news....

{{ JSON.stringify($json.data, null, 2) }}

Your output is sent directly to my mate on discord, so just give a brief, friendly suggestion on what to do today from a forex perspective.  We are normally looking for opportunities to short the EUR/USD so if you see some news that might be worth us looking into for that let us know, but we only really trade the news so if you don't see anything of interest you can just let us know."""
    
    SYNTHESIS_PROMPT = """I have several AI agents giving me their feedback on the market today. Each agent has a different perspective and temperature setting, so they may emphasize different aspects. Can you synthesize all these views into ONE clear recommendation?

Here are the agent analyses:

{{ JSON.stringify($json.data, null, 2) }}

Send me your thoughts on discord... I'll just pass them directly, so just say what you need to say... don't loose me any money. :) 

make sure you explain any acronyms, and any risk/reward.  I am new to this, you need to spell everything out for me.  base my actions on £100 investment, not leveraged. so if I trade, and we make a short, what would I gain/loose or risk in raw pound notes. give me the odds, in a clear and understandable way. 

If the agents disagree, note that and explain the different viewpoints briefly, then give your best judgment.

We are limited on characters though, as we're sending to discord, so follow BLUF (bottom line up front), forget niceties, and just give me what I need to know... shorter the better."""
    
    def __init__(self, ollama_base_url: str, models_with_temps: List[tuple[str, float]], 
                 synthesis_model: str, synthesis_temp: float, run_concurrent: bool):
        self.ollama_base_url = ollama_base_url
        self.models_with_temps = models_with_temps
        self.synthesis_model = synthesis_model
        self.synthesis_temp = synthesis_temp
        self.run_concurrent = run_concurrent
    
    def analyze_news(self, aggregated_data: Dict[str, Any]) -> str:
        """Run multiple AI analyses and synthesize results."""
        
        mode = "Concurrent" if self.run_concurrent else "Sequential"
        console.print(f"\n[bold cyan]Starting AI Analysis ({mode} Mode)[/bold cyan]\n")
        
        if self.run_concurrent:
            return asyncio.run(self._analyze_news_async(aggregated_data))
        else:
            return self._analyze_news_sequential(aggregated_data)
    
    def _analyze_news_sequential(self, aggregated_data: Dict[str, Any]) -> str:
        """Sequential analysis - better for Ollama instances that can't handle concurrent requests."""
        
        # Create analyzers with diverse models and temperatures
        analyzers = []
        for idx, (model, temp) in enumerate(self.models_with_temps, 1):
            name = f"Agent {idx} ({model.split(':')[0]} @ temp={temp})"
            analyzers.append((name, OllamaAnalyzer(self.ollama_base_url, model, temp)))
        
        analyses = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running AI analyses sequentially...", total=len(analyzers) + 1)
            
            # Run analyses one by one
            for name, analyzer in analyzers:
                progress.update(task, description=f"[cyan]{name} analyzing...")
                
                # Use synchronous analyze for sequential mode
                result = asyncio.run(analyzer.analyze_async(self.ANALYSIS_PROMPT, aggregated_data))
                
                analyses.append({
                    "agent": name,
                    "output": result
                })
                progress.advance(task)
                console.print(f"[green]✓[/green] {name} complete")
            
            # Synthesize all analyses
            progress.update(task, description="[cyan]Synthesizing results...")
            synthesis_data = {"data": analyses}
            final_analyzer = OllamaAnalyzer(self.ollama_base_url, self.synthesis_model, self.synthesis_temp)
            final_result = asyncio.run(final_analyzer.analyze_async(self.SYNTHESIS_PROMPT, synthesis_data))
            progress.advance(task)
            console.print(f"[green]✓[/green] Synthesis complete\n")
        
        return final_result
    
    async def _analyze_news_async(self, aggregated_data: Dict[str, Any]) -> str:
        """Concurrent analysis - faster but requires Ollama to handle parallel requests."""
        
        # Create analyzers with diverse models and temperatures
        analyzers = []
        for idx, (model, temp) in enumerate(self.models_with_temps, 1):
            name = f"Agent {idx} ({model.split(':')[0]} @ temp={temp})"
            analyzers.append((name, OllamaAnalyzer(self.ollama_base_url, model, temp)))
        
        analyses = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running AI analyses concurrently...", total=len(analyzers) + 1)
            
            # Create async tasks for all agents
            agent_tasks = []
            for name, analyzer in analyzers:
                agent_tasks.append(self._run_agent_analysis(name, analyzer, aggregated_data))
            
            # Run all agent analyses concurrently
            console.print(f"[dim]Running {len(analyzers)} agents in parallel...[/dim]")
            agent_results = await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            # Collect results
            for result in agent_results:
                if isinstance(result, Exception):
                    console.print(f"[red]✗[/red] Agent failed: {str(result)}")
                    continue
                    
                name, output = result
                analyses.append({
                    "agent": name,
                    "output": output
                })
                progress.advance(task, advance=1)
                console.print(f"[green]✓[/green] {name} complete")
            
            # Synthesize all analyses
            progress.update(task, description="[cyan]Synthesizing results...")
            synthesis_data = {"data": analyses}
            final_analyzer = OllamaAnalyzer(self.ollama_base_url, self.synthesis_model, self.synthesis_temp)
            final_result = await final_analyzer.analyze_async(self.SYNTHESIS_PROMPT, synthesis_data)
            progress.advance(task)
            console.print(f"[green]✓[/green] Synthesis complete\n")
        
        return final_result
    
    async def _run_agent_analysis(self, name: str, analyzer: OllamaAnalyzer, data: Dict[str, Any]) -> tuple:
        """Run a single agent analysis asynchronously."""
        result = await analyzer.analyze_async(self.ANALYSIS_PROMPT, data)
        return (name, result)
