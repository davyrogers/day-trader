"""AI analysis module using Ollama for forex news analysis."""
import json
import asyncio
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from dataclasses import dataclass
from market_data import MarketDataFetcher, extract_instrument_from_news

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
    
    def __init__(self, ollama_base_url: str, run_concurrent: bool, config_path: Optional[str] = None, market_data_api_key: Optional[str] = None):
        self.ollama_base_url = ollama_base_url
        self.run_concurrent = run_concurrent
        
        # Setup reports directory
        self.reports_dir = Path(__file__).parent.parent / "reports"
        self._setup_reports_directory()
        
        # Load team configuration from JSON
        self.team_config = TeamConfiguration(config_path)
        self.junior_analysts = self.team_config.junior_analysts
        self.senior_managers = [layer for layer in self.team_config.management_layers 
                               if 'senior' in layer.name.lower() or 'manager' in layer.name.lower() and 'executive' not in layer.name.lower()]
        self.executive_committees = [layer for layer in self.team_config.management_layers 
                                     if 'executive' in layer.name.lower() or 'committee' in layer.name.lower()]
        
        # Initialize market data fetcher
        self.market_data_fetcher = MarketDataFetcher(api_key=market_data_api_key)
        
        if not self.senior_managers:
            console.print("[yellow]Warning: No senior managers found in config, using first management layer[/yellow]")
            self.senior_managers = [self.team_config.management_layers[0]] if self.team_config.management_layers else []
        if not self.executive_committees:
            console.print("[yellow]Warning: No executive committees found in config, using last management layer[/yellow]")
            self.executive_committees = [self.team_config.management_layers[-1]] if len(self.team_config.management_layers) > 1 else []
    
    def _setup_reports_directory(self):
        """Clear and setup the reports directory for a fresh run."""
        if self.reports_dir.exists():
            # Clear existing reports
            shutil.rmtree(self.reports_dir)
        
        # Create fresh directory structure
        self.reports_dir.mkdir(exist_ok=True)
        (self.reports_dir / "tier1_junior_analysts").mkdir(exist_ok=True)
        (self.reports_dir / "tier2_senior_managers").mkdir(exist_ok=True)
        (self.reports_dir / "tier3_executive_committees").mkdir(exist_ok=True)
        
        console.print(f"[green]✓[/green] Reports directory cleared and ready: {self.reports_dir}")
    
    def _save_report(self, tier: str, name: str, role: str, content: str, order: int = None):
        """Save an individual report to the reports directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Sanitize filename
        safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)
        safe_name = safe_name.replace(' ', '_')
        
        # Build filename with order if provided
        if order is not None:
            filename = f"{order:02d}_{safe_name}_{timestamp}.txt"
        else:
            filename = f"{safe_name}_{timestamp}.txt"
        
        filepath = self.reports_dir / tier / filename
        
        # Write report with header
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{'='*80}\n")
            f.write(f"{name}\n")
            f.write(f"Role: {role}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            f.write(content)
        
        console.print(f"[dim]  → Saved report: {filepath.name}[/dim]")

    
    def analyze_news(self, aggregated_data: Dict[str, Any]) -> str:
        """Run multi-tier analysis: Junior Analysts → Senior Managers → Executive Committees."""
        
        mode = "Concurrent" if self.run_concurrent else "Sequential"
        console.print(f"\n[bold cyan]Starting Enhanced Multi-Tier AI Analysis Pipeline ({mode} Mode)[/bold cyan]")
        console.print(f"[dim]Tier 1: {len(self.junior_analysts)} Junior Analysts[/dim]")
        console.print(f"[dim]Tier 2: {len(self.senior_managers)} Senior Managers[/dim]")
        console.print(f"[dim]Tier 3: {len(self.executive_committees)} Executive Committees[/dim]\n")
        
        if self.run_concurrent:
            return asyncio.run(self._analyze_news_async(aggregated_data))
        else:
            return self._analyze_news_sequential(aggregated_data)
    
    def _analyze_news_sequential(self, aggregated_data: Dict[str, Any]) -> str:
        """Sequential multi-tier analysis pipeline with market data integration."""
        
        # Fetch market data first
        console.print("[bold cyan]Fetching real-time market data...[/bold cyan]")
        instrument = extract_instrument_from_news(aggregated_data)
        market_data_raw = asyncio.run(self.market_data_fetcher.get_forex_data_async(instrument))
        market_data_formatted = self.market_data_fetcher.format_market_data(market_data_raw)
        console.print(market_data_formatted)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            total_steps = len(self.junior_analysts) + len(self.senior_managers) + len(self.executive_committees)
            task = progress.add_task("[cyan]Running analysis pipeline...", total=total_steps)
            
            # TIER 1: Junior Analysts Review
            console.print("[bold yellow]═══ TIER 1: JUNIOR ANALYSTS ═══[/bold yellow]")
            junior_reports = []
            
            for idx, analyst in enumerate(self.junior_analysts, 1):
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
                
                # Save individual report
                self._save_report("tier1_junior_analysts", analyst.name, analyst.role, result, order=idx)
                
                junior_reports.append({
                    "analyst": analyst.name,
                    "role": analyst.role,
                    "focus": analyst.focus_area,
                    "output": result
                })
                progress.advance(task)
                console.print(f"[green]✓[/green] {analyst.name} report complete")
            
            # TIER 2: Senior Manager Synthesis (Multiple Managers)
            if not self.senior_managers:
                console.print("[red]Error: No senior managers configured[/red]")
                return "Configuration error: No senior managers found"
            
            console.print(f"\n[bold yellow]═══ TIER 2: SENIOR MANAGERS ({len(self.senior_managers)} Managers) ═══[/bold yellow]")
            senior_reports = []
            
            for idx, manager in enumerate(self.senior_managers, 1):
                progress.update(task, description=f"[cyan]{manager.name} synthesizing...")
                
                senior_data = {"data": junior_reports}
                
                # Inject market data into prompt
                manager_prompt = manager.system_prompt.replace("{{MARKET_DATA}}", market_data_formatted)
                
                senior_analyzer = OllamaAnalyzer(
                    self.ollama_base_url,
                    manager.model,
                    manager.temperature
                )
                senior_report = asyncio.run(
                    senior_analyzer.analyze_async(manager_prompt, senior_data)
                )
                
                # Save individual report
                self._save_report("tier2_senior_managers", manager.name, manager.role, senior_report, order=idx)
                
                senior_reports.append({
                    "manager": manager.name,
                    "role": manager.role,
                    "output": senior_report
                })
                progress.advance(task)
                console.print(f"[green]✓[/green] {manager.name} synthesis complete")
            
            # TIER 3: Executive Committee Final Review (Multiple Committees)
            if not self.executive_committees:
                console.print("[red]Error: No executive committees configured[/red]")
                return senior_reports[0]['output'] if senior_reports else "Error: No reports generated"
            
            console.print(f"\n[bold yellow]═══ TIER 3: EXECUTIVE COMMITTEES ({len(self.executive_committees)} Committees) ═══[/bold yellow]")
            final_decisions = []
            
            for idx, committee in enumerate(self.executive_committees, 1):
                progress.update(task, description=f"[cyan]{committee.name} deliberating...")
                
                executive_data = {
                    "data": {
                        "senior_reports": senior_reports,
                        "analyst_count": len(junior_reports),
                        "manager_count": len(senior_reports)
                    }
                }
                
                # Inject market data into prompt
                committee_prompt = committee.system_prompt.replace("{{MARKET_DATA}}", market_data_formatted)
                
                executive_analyzer = OllamaAnalyzer(
                    self.ollama_base_url,
                    committee.model,
                    committee.temperature
                )
                final_decision = asyncio.run(
                    executive_analyzer.analyze_async(committee_prompt, executive_data)
                )
                
                # Save individual report
                self._save_report("tier3_executive_committees", committee.name, committee.role, final_decision, order=idx)
                
                final_decisions.append({
                    "committee": committee.name,
                    "role": committee.role,
                    "output": final_decision
                })
                progress.advance(task)
                console.print(f"[green]✓[/green] {committee.name} decision complete")
        
        # Return all executive decisions with clear separation
        result = "\n\n" + "="*80 + "\n"
        result += "FINAL EXECUTIVE DECISIONS\n"
        result += "="*80 + "\n\n"
        
        for i, decision in enumerate(final_decisions, 1):
            result += f"\n{'─'*80}\n"
            result += f"{decision['committee']} ({decision['role']})\n"
            result += f"{'─'*80}\n\n"
            result += decision['output']
            result += "\n"
        
        result += "\n" + "="*80 + "\n"
        
        # Save final summary (sequential mode)
        self._save_final_summary(result, junior_reports, senior_reports, final_decisions)
        
        return result
    
    async def _analyze_news_async(self, aggregated_data: Dict[str, Any]) -> str:
        """Concurrent multi-tier analysis pipeline with market data integration."""
        
        # Fetch market data first
        console.print("[bold cyan]Fetching real-time market data...[/bold cyan]")
        instrument = extract_instrument_from_news(aggregated_data)
        market_data_raw = await self.market_data_fetcher.get_forex_data_async(instrument)
        market_data_formatted = self.market_data_fetcher.format_market_data(market_data_raw)
        console.print(market_data_formatted)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            total_steps = len(self.junior_analysts) + len(self.senior_managers) + len(self.executive_committees)
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
            for idx, result in enumerate(analyst_results, 1):
                if isinstance(result, Exception):
                    console.print(f"[red]✗[/red] Analyst failed: {str(result)}")
                    continue
                
                analyst_name, analyst_role, focus_area, output = result
                
                # Save individual report
                self._save_report("tier1_junior_analysts", analyst_name, analyst_role, output, order=idx)
                
                junior_reports.append({
                    "analyst": analyst_name,
                    "role": analyst_role,
                    "focus": focus_area,
                    "output": output
                })
                progress.advance(task, advance=1)
                console.print(f"[green]✓[/green] {analyst_name} report complete")
            
            # TIER 2: Senior Manager Synthesis (Multiple Managers, run concurrently)
            if not self.senior_managers:
                console.print("[red]Error: No senior managers configured[/red]")
                return "Configuration error: No senior managers found"
            
            console.print(f"\n[bold yellow]═══ TIER 2: SENIOR MANAGERS (CONCURRENT - {len(self.senior_managers)} Managers) ═══[/bold yellow]")
            
            manager_tasks = []
            for manager in self.senior_managers:
                senior_data = {"data": junior_reports}
                # Inject market data into prompt
                manager_prompt = manager.system_prompt.replace("{{MARKET_DATA}}", market_data_formatted)
                
                senior_analyzer = OllamaAnalyzer(
                    self.ollama_base_url,
                    manager.model,
                    manager.temperature
                )
                manager_tasks.append(
                    self._run_senior_manager(manager, senior_analyzer, manager_prompt, senior_data)
                )
            
            # Run all senior managers concurrently
            manager_results = await asyncio.gather(*manager_tasks, return_exceptions=True)
            
            senior_reports = []
            for idx, result in enumerate(manager_results, 1):
                if isinstance(result, Exception):
                    console.print(f"[red]✗[/red] Manager failed: {str(result)}")
                    continue
                
                manager_name, manager_role, output = result
                
                # Save individual report
                self._save_report("tier2_senior_managers", manager_name, manager_role, output, order=idx)
                
                senior_reports.append({
                    "manager": manager_name,
                    "role": manager_role,
                    "output": output
                })
                progress.advance(task, advance=1)
                console.print(f"[green]✓[/green] {manager_name} synthesis complete")
            
            # TIER 3: Executive Committee Final Review (Multiple Committees, run concurrently)
            if not self.executive_committees:
                console.print("[red]Error: No executive committees configured[/red]")
                return senior_reports[0]['output'] if senior_reports else "Error: No reports generated"
            
            console.print(f"\n[bold yellow]═══ TIER 3: EXECUTIVE COMMITTEES (CONCURRENT - {len(self.executive_committees)} Committees) ═══[/bold yellow]")
            
            committee_tasks = []
            for committee in self.executive_committees:
                executive_data = {
                    "data": {
                        "senior_reports": senior_reports,
                        "analyst_count": len(junior_reports),
                        "manager_count": len(senior_reports)
                    }
                }
                
                # Inject market data into prompt
                committee_prompt = committee.system_prompt.replace("{{MARKET_DATA}}", market_data_formatted)
                
                executive_analyzer = OllamaAnalyzer(
                    self.ollama_base_url,
                    committee.model,
                    committee.temperature
                )
                committee_tasks.append(
                    self._run_executive_committee(committee, executive_analyzer, committee_prompt, executive_data)
                )
            
            # Run all executive committees concurrently
            committee_results = await asyncio.gather(*committee_tasks, return_exceptions=True)
            
            final_decisions = []
            for idx, result in enumerate(committee_results, 1):
                if isinstance(result, Exception):
                    console.print(f"[red]✗[/red] Committee failed: {str(result)}")
                    continue
                
                committee_name, committee_role, output = result
                
                # Save individual report
                self._save_report("tier3_executive_committees", committee_name, committee_role, output, order=idx)
                
                final_decisions.append({
                    "committee": committee_name,
                    "role": committee_role,
                    "output": output
                })
                progress.advance(task, advance=1)
                console.print(f"[green]✓[/green] {committee_name} decision complete")
        
        # Return all executive decisions with clear separation
        result = "\n\n" + "="*80 + "\n"
        result += "FINAL EXECUTIVE DECISIONS\n"
        result += "="*80 + "\n\n"
        
        for i, decision in enumerate(final_decisions, 1):
            result += f"\n{'─'*80}\n"
            result += f"{decision['committee']} ({decision['role']})\n"
            result += f"{'─'*80}\n\n"
            result += decision['output']
            result += "\n"
        
        result += "\n" + "="*80 + "\n"
        
        # Save final summary (concurrent mode)
        self._save_final_summary(result, junior_reports, senior_reports, final_decisions)
        
        return result
    
    async def _run_junior_analyst(self, analyst: AnalystProfile, analyzer: OllamaAnalyzer, 
                                   prompt: str, data: Dict[str, Any]) -> tuple:
        """Run a single junior analyst analysis asynchronously."""
        result = await analyzer.analyze_async(prompt, data)
        return (analyst.name, analyst.role, analyst.focus_area, result)
    
    async def _run_senior_manager(self, manager: ManagementLayer, analyzer: OllamaAnalyzer,
                                   prompt: str, data: Dict[str, Any]) -> tuple:
        """Run a single senior manager synthesis asynchronously."""
        result = await analyzer.analyze_async(prompt, data)
        return (manager.name, manager.role, result)
    
    async def _run_executive_committee(self, committee: ManagementLayer, analyzer: OllamaAnalyzer,
                                        prompt: str, data: Dict[str, Any]) -> tuple:
        """Run a single executive committee review asynchronously."""
        result = await analyzer.analyze_async(prompt, data)
        return (committee.name, committee.role, result)
    
    def _save_final_summary(self, result: str, junior_reports: List[Dict], 
                           senior_reports: List[Dict], final_decisions: List[Dict]):
        """Save a comprehensive summary of the entire analysis run."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.reports_dir / f"FINAL_SUMMARY_{timestamp}.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{'='*80}\n")
            f.write(f"COMPLETE ANALYSIS SUMMARY\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            
            f.write(f"PIPELINE STATISTICS:\n")
            f.write(f"  • Junior Analysts: {len(junior_reports)}\n")
            f.write(f"  • Senior Managers: {len(senior_reports)}\n")
            f.write(f"  • Executive Committees: {len(final_decisions)}\n\n")
            
            f.write(f"{'='*80}\n")
            f.write(f"EXECUTIVE DECISIONS (SENT TO DISCORD)\n")
            f.write(f"{'='*80}\n")
            f.write(result)
            
            f.write(f"\n\n{'='*80}\n")
            f.write(f"DETAILED BREAKDOWN\n")
            f.write(f"{'='*80}\n\n")
            
            f.write(f"All individual reports are saved in:\n")
            f.write(f"  • {self.reports_dir / 'tier1_junior_analysts'}\n")
            f.write(f"  • {self.reports_dir / 'tier2_senior_managers'}\n")
            f.write(f"  • {self.reports_dir / 'tier3_executive_committees'}\n")
        
        console.print(f"\n[bold green]✓ Complete analysis saved to: {filepath}[/bold green]")


