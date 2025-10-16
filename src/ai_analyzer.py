"""AI analysis module using Ollama for forex news analysis."""
import json
import asyncio
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from dataclasses import dataclass

console = Console()


@dataclass
class AnalystProfile:
    """Defines an AI analyst's personality and behavior."""
    name: str
    role: str
    personality: str
    model: str
    temperature: float
    focus_area: str
    system_prompt: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AnalystProfile':
        """Create AnalystProfile from dictionary."""
        return cls(
            name=data['name'],
            role=data['role'],
            personality=data['personality'],
            model=data['model'],
            temperature=data['temperature'],
            focus_area=data['focus_area'],
            system_prompt=data['system_prompt']
        )


@dataclass
class ManagementLayer:
    """Defines a management layer (Senior Manager or Executive Committee)."""
    name: str
    role: str
    model: str
    temperature: float
    system_prompt: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ManagementLayer':
        """Create ManagementLayer from dictionary."""
        return cls(
            name=data['name'],
            role=data['role'],
            model=data['model'],
            temperature=data['temperature'],
            system_prompt=data['system_prompt']
        )


class TeamConfiguration:
    """Loads and manages analyst team configuration from JSON."""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default to analyst_team.json in project root
            current_dir = Path(__file__).parent.parent
            config_path = current_dir / "analyst_team.json"
        
        self.config_path = Path(config_path)
        self.junior_analysts: List[AnalystProfile] = []
        self.management_layers: List[ManagementLayer] = []
        self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Load junior analysts
            for analyst_data in config.get('junior_analysts', []):
                self.junior_analysts.append(AnalystProfile.from_dict(analyst_data))
            
            # Load management layers
            for mgmt_data in config.get('management_layers', []):
                self.management_layers.append(ManagementLayer.from_dict(mgmt_data))
            
            console.print(f"[green]✓[/green] Loaded {len(self.junior_analysts)} analysts and {len(self.management_layers)} management layers from config")
            
        except FileNotFoundError:
            console.print(f"[red]Error: Configuration file not found at {self.config_path}[/red]")
            raise
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing configuration JSON: {e}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]Error loading configuration: {e}[/red]")
            raise
    
    def get_senior_manager(self) -> Optional[ManagementLayer]:
        """Get the senior manager layer."""
        for layer in self.management_layers:
            if 'senior' in layer.name.lower() or 'manager' in layer.name.lower():
                return layer
        return self.management_layers[0] if self.management_layers else None
    
    def get_executive_committee(self) -> Optional[ManagementLayer]:
        """Get the executive committee layer."""
        for layer in self.management_layers:
            if 'executive' in layer.name.lower() or 'committee' in layer.name.lower():
                return layer
        return self.management_layers[-1] if len(self.management_layers) > 1 else None


class OllamaAnalyzer:
    """Handles AI analysis using Ollama models."""
    
    def __init__(self, base_url: str, model: str, temperature: float = 0.8, analyst_profile: Optional[AnalystProfile] = None):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.analyst_profile = analyst_profile
    
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
    """Orchestrates multi-tier AI analysis with junior analysts, senior synthesis, and executive review."""
    
    def __init__(self, ollama_base_url: str, run_concurrent: bool, config_path: Optional[str] = None):
        self.ollama_base_url = ollama_base_url
        self.run_concurrent = run_concurrent
        
        # Load team configuration from JSON
        self.team_config = TeamConfiguration(config_path)
        self.junior_analysts = self.team_config.junior_analysts
        self.senior_manager = self.team_config.get_senior_manager()
        self.executive_committee = self.team_config.get_executive_committee()
        
        if not self.senior_manager:
            console.print("[yellow]Warning: No senior manager found in config, using default[/yellow]")
        if not self.executive_committee:
            console.print("[yellow]Warning: No executive committee found in config, using default[/yellow]")
    
    def analyze_news(self, aggregated_data: Dict[str, Any]) -> str:
        """Run three-tier analysis: Junior Analysts → Senior Manager → Executive Committee."""
        
        mode = "Concurrent" if self.run_concurrent else "Sequential"
        console.print(f"\n[bold cyan]Starting 3-Tier AI Analysis Pipeline ({mode} Mode)[/bold cyan]")
        console.print(f"[dim]Tier 1: {len(self.junior_analysts)} Junior Analysts[/dim]")
        console.print(f"[dim]Tier 2: Senior Manager Synthesis[/dim]")
        console.print(f"[dim]Tier 3: Executive Committee Review[/dim]\n")
        
        if self.run_concurrent:
            return asyncio.run(self._analyze_news_async(aggregated_data))
        else:
            return self._analyze_news_sequential(aggregated_data)
    
    def _analyze_news_sequential(self, aggregated_data: Dict[str, Any]) -> str:
        """Sequential three-tier analysis pipeline."""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            total_steps = len(self.junior_analysts) + 2  # analysts + senior + executive
            task = progress.add_task("[cyan]Running analysis pipeline...", total=total_steps)
            
            # TIER 1: Junior Analysts Review
            console.print("[bold yellow]═══ TIER 1: JUNIOR ANALYSTS ═══[/bold yellow]")
            junior_reports = []
            
            for analyst in self.junior_analysts:
                progress.update(task, description=f"[cyan]{analyst.name} analyzing...")
                
                # Use analyst's configured system prompt
                prompt = analyst.system_prompt
                analyzer = OllamaAnalyzer(
                    self.ollama_base_url, 
                    analyst.model, 
                    analyst.temperature,
                    analyst
                )
                
                result = asyncio.run(analyzer.analyze_async(prompt, aggregated_data))
                
                junior_reports.append({
                    "analyst": analyst.name,
                    "role": analyst.role,
                    "focus": analyst.focus_area,
                    "output": result
                })
                progress.advance(task)
                console.print(f"[green]✓[/green] {analyst.name} report complete")
            
            # TIER 2: Senior Manager Synthesis
            if not self.senior_manager:
                console.print("[red]Error: No senior manager configured[/red]")
                return "Configuration error: No senior manager found"
            
            console.print("\n[bold yellow]═══ TIER 2: SENIOR MANAGER ═══[/bold yellow]")
            progress.update(task, description="[cyan]Senior Manager synthesizing reports...")
            
            senior_data = {"data": junior_reports}
            senior_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.senior_manager.model,
                self.senior_manager.temperature
            )
            senior_report = asyncio.run(
                senior_analyzer.analyze_async(self.senior_manager.system_prompt, senior_data)
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] {self.senior_manager.name} synthesis complete")
            
            # TIER 3: Executive Committee Final Review
            if not self.executive_committee:
                console.print("[red]Error: No executive committee configured[/red]")
                return senior_report  # Return senior report if no exec committee
            
            console.print("\n[bold yellow]═══ TIER 3: EXECUTIVE COMMITTEE ═══[/bold yellow]")
            progress.update(task, description="[cyan]Executive Committee deliberating...")
            
            executive_data = {"data": {"senior_report": senior_report, "analyst_count": len(junior_reports)}}
            executive_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.executive_committee.model,
                self.executive_committee.temperature
            )
            final_decision = asyncio.run(
                executive_analyzer.analyze_async(self.executive_committee.system_prompt, executive_data)
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] {self.executive_committee.name} decision complete\n")
        
        return final_decision
    
    async def _analyze_news_async(self, aggregated_data: Dict[str, Any]) -> str:
        """Concurrent three-tier analysis pipeline."""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            total_steps = len(self.junior_analysts) + 2
            task = progress.add_task("[cyan]Running analysis pipeline...", total=total_steps)
            
            # TIER 1: Junior Analysts Review (Concurrent)
            console.print("[bold yellow]═══ TIER 1: JUNIOR ANALYSTS (CONCURRENT) ═══[/bold yellow]")
            console.print(f"[dim]Running {len(self.junior_analysts)} analysts in parallel...[/dim]")
            
            analyst_tasks = []
            for analyst in self.junior_analysts:
                # Use analyst's configured system prompt
                prompt = analyst.system_prompt
                analyzer = OllamaAnalyzer(
                    self.ollama_base_url,
                    analyst.model,
                    analyst.temperature,
                    analyst
                )
                analyst_tasks.append(
                    self._run_junior_analyst(analyst, analyzer, prompt, aggregated_data)
                )
            
            # Run all junior analysts concurrently
            analyst_results = await asyncio.gather(*analyst_tasks, return_exceptions=True)
            
            junior_reports = []
            for result in analyst_results:
                if isinstance(result, Exception):
                    console.print(f"[red]✗[/red] Analyst failed: {str(result)}")
                    continue
                
                analyst_name, analyst_role, focus_area, output = result
                junior_reports.append({
                    "analyst": analyst_name,
                    "role": analyst_role,
                    "focus": focus_area,
                    "output": output
                })
                progress.advance(task, advance=1)
                console.print(f"[green]✓[/green] {analyst_name} report complete")
            
            # TIER 2: Senior Manager Synthesis
            if not self.senior_manager:
                console.print("[red]Error: No senior manager configured[/red]")
                return "Configuration error: No senior manager found"
            
            console.print("\n[bold yellow]═══ TIER 2: SENIOR MANAGER ═══[/bold yellow]")
            progress.update(task, description="[cyan]Senior Manager synthesizing reports...")
            
            senior_data = {"data": junior_reports}
            senior_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.senior_manager.model,
                self.senior_manager.temperature
            )
            senior_report = await senior_analyzer.analyze_async(
                self.senior_manager.system_prompt, senior_data
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] {self.senior_manager.name} synthesis complete")
            
            # TIER 3: Executive Committee Final Review
            if not self.executive_committee:
                console.print("[red]Error: No executive committee configured[/red]")
                return senior_report  # Return senior report if no exec committee
            
            console.print("\n[bold yellow]═══ TIER 3: EXECUTIVE COMMITTEE ═══[/bold yellow]")
            progress.update(task, description="[cyan]Executive Committee deliberating...")
            
            executive_data = {"data": {"senior_report": senior_report, "analyst_count": len(junior_reports)}}
            executive_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.executive_committee.model,
                self.executive_committee.temperature
            )
            final_decision = await executive_analyzer.analyze_async(
                self.executive_committee.system_prompt, executive_data
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] {self.executive_committee.name} decision complete\n")
        
        return final_decision
    
    async def _run_junior_analyst(self, analyst: AnalystProfile, analyzer: OllamaAnalyzer, 
                                   prompt: str, data: Dict[str, Any]) -> tuple:
        """Run a single junior analyst analysis asynchronously."""
        result = await analyzer.analyze_async(prompt, data)
        return (analyst.name, analyst.role, analyst.focus_area, result)
