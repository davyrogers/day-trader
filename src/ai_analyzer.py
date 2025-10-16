"""AI analysis module using Ollama for forex news analysis."""
import json
import asyncio
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
    
    
class AIAnalystTeam:
    """Defines the team of junior analysts with diverse perspectives."""
    
    ANALYSTS = [
        AnalystProfile(
            name="Marcus (Conservative)",
            role="Risk Management Specialist",
            personality="Conservative, risk-averse, focuses on downside protection",
            model="llama3.2:latest",
            temperature=0.3,
            focus_area="Risk assessment and capital preservation"
        ),
        AnalystProfile(
            name="Sarah (Technical)",
            role="Technical Analysis Expert",
            personality="Data-driven, pattern-focused, relies on technical indicators",
            model="qwen2.5:latest",
            temperature=0.5,
            focus_area="Chart patterns, support/resistance levels, technical signals"
        ),
        AnalystProfile(
            name="James (Aggressive)",
            role="Momentum Trader",
            personality="Aggressive, opportunity-seeking, high-conviction trades",
            model="mistral:latest",
            temperature=0.8,
            focus_area="High-probability momentum plays and breakouts"
        ),
        AnalystProfile(
            name="Elena (Fundamental)",
            role="Economic Policy Analyst",
            personality="Fundamental-focused, macro-economic perspective, central bank watcher",
            model="llama3.2:latest",
            temperature=0.4,
            focus_area="Economic indicators, central bank policy, geopolitical events"
        ),
        AnalystProfile(
            name="David (Contrarian)",
            role="Contrarian Strategist",
            personality="Skeptical, contrarian, questions consensus views",
            model="gemma2:latest",
            temperature=0.7,
            focus_area="Identifying overcrowded trades and contrary indicators"
        ),
        AnalystProfile(
            name="Priya (Sentiment)",
            role="Market Sentiment Analyst",
            personality="Sentiment-focused, reads market mood, tracks positioning",
            model="phi3:latest",
            temperature=0.6,
            focus_area="Market sentiment, trader positioning, fear/greed indicators"
        ),
    ]
    
    @classmethod
    def get_analyst_prompt(cls, analyst: AnalystProfile) -> str:
        """Generate a personalized prompt for each analyst."""
        return f"""You are {analyst.name}, a {analyst.role} on a professional forex trading desk.

PERSONALITY: {analyst.personality}
YOUR FOCUS: {analyst.focus_area}

Today's market news is below. Review it from YOUR unique perspective and provide YOUR professional opinion.

CRITICAL REQUIREMENTS:
- Focus on EUR/USD trading opportunities (we primarily short EUR/USD with the trend)
- Identify SPECIFIC timing windows for potential trades (exact times in UTC/GMT)
- Note any high-impact economic data releases with precise times
- Flag volatility risks and time periods to avoid trading
- We trade WITH major trends, never against them
- Look for news-driven opportunities for small, lower-risk profits

YOUR ANALYSIS MUST INCLUDE:
1. Key news events TODAY with EXACT TIMES
2. Your view on EUR/USD direction and timing
3. Risk factors specific to your expertise
4. Confidence level (Low/Medium/High) for any trade ideas

NEWS DATA:
{{{{ JSON.stringify($json.data, null, 2) }}}}

REMEMBER: You're reporting to senior management. Be professional but concise. If you see nothing actionable, say so clearly."""


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
    
    SENIOR_SYNTHESIS_PROMPT = """You are the SENIOR TRADING MANAGER reviewing reports from your team of 6 junior analysts.

Each analyst has provided their perspective on today's forex market (focusing on EUR/USD). Your job is to:

1. SYNTHESIZE their views into a coherent picture
2. IDENTIFY points of agreement and disagreement
3. NOTE any time-specific opportunities they've flagged
4. FILTER OUT noise and conflicting signals
5. HIGHLIGHT consensus trade ideas with specific timing

ANALYST REPORTS:
{{ JSON.stringify($json.data, null, 2) }}

SENIOR MANAGER OUTPUT REQUIREMENTS:
- Consolidate the key events and times mentioned by multiple analysts
- Identify if there's consensus on EUR/USD direction
- Note divergent views and explain why they differ
- Recommend IF we should be watching for a trade opportunity today
- Specify WHEN (exact time windows in UTC/GMT)
- Keep it professional but concise - this goes to the executive committee

If analysts disagree significantly, note this and explain both sides."""

    EXECUTIVE_COMMITTEE_PROMPT = """You are the EXECUTIVE TRADING COMMITTEE (3 senior partners) reviewing the consolidated report from your senior manager.

The senior manager has synthesized input from 6 junior analysts. Now you must make the FINAL DECISION on actionable trades.

SENIOR MANAGER'S REPORT:
{{ JSON.stringify($json.data, null, 2) }}

YOUR EXECUTIVE RESPONSIBILITIES:
1. DEBATE the merits of any proposed trades among yourselves
2. VERIFY timing and risk/reward calculations  
3. FILTER OUT any remaining noise or uncertain signals
4. BUILD CONSENSUS on specific trade recommendations
5. PROVIDE CLEAR, ACTIONABLE GUIDANCE

OUTPUT FORMAT FOR DISCORD (Character limit: keep it tight!):
━━━━━━━━━━━━━━━━━━━━
🎯 TRADING SIGNAL - [DATE]
━━━━━━━━━━━━━━━━━━━━

📊 CONSENSUS: [Clear Yes/No/Watch on trade opportunity]

⏰ KEY TIMES (UTC):
[List 2-3 most critical time windows only]

💹 TRADE SETUP (if applicable):
Pair: EUR/USD
Direction: [Long/Short]
Entry timing: [Specific time window]
Risk: £X on £100 position
Reward: £Y potential
Odds: [X%] based on [reason]

⚠️ RISKS:
[Top 2-3 risks only]

🎲 EXECUTIVE DECISION:
[Clear 2-3 sentence recommendation - what should trader DO today]

━━━━━━━━━━━━━━━━━━━━

CRITICAL RULES:
- Use BLUF format (bottom line up front)
- Explain ALL acronyms in parentheses  
- Base risk/reward on £100 un-leveraged position
- If consensus is "NO TRADE", say why clearly
- If committee is divided, note the split and give majority view
- Keep total message under 1500 characters for Discord"""

    def __init__(self, ollama_base_url: str, run_concurrent: bool):
        self.ollama_base_url = ollama_base_url
        self.run_concurrent = run_concurrent
        self.junior_analysts = AIAnalystTeam.ANALYSTS
        # Senior and Executive use more stable, analytical models
        self.senior_model = "llama3.2:latest"
        self.senior_temp = 0.4
        self.executive_model = "llama3.2:latest" 
        self.executive_temp = 0.3  # Very conservative for final decisions
    
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
                
                prompt = AIAnalystTeam.get_analyst_prompt(analyst)
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
            console.print("\n[bold yellow]═══ TIER 2: SENIOR MANAGER ═══[/bold yellow]")
            progress.update(task, description="[cyan]Senior Manager synthesizing reports...")
            
            senior_data = {"data": junior_reports}
            senior_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.senior_model,
                self.senior_temp
            )
            senior_report = asyncio.run(
                senior_analyzer.analyze_async(self.SENIOR_SYNTHESIS_PROMPT, senior_data)
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] Senior Manager synthesis complete")
            
            # TIER 3: Executive Committee Final Review
            console.print("\n[bold yellow]═══ TIER 3: EXECUTIVE COMMITTEE ═══[/bold yellow]")
            progress.update(task, description="[cyan]Executive Committee deliberating...")
            
            executive_data = {"data": {"senior_report": senior_report, "analyst_count": len(junior_reports)}}
            executive_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.executive_model,
                self.executive_temp
            )
            final_decision = asyncio.run(
                executive_analyzer.analyze_async(self.EXECUTIVE_COMMITTEE_PROMPT, executive_data)
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] Executive Committee decision complete\n")
        
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
                prompt = AIAnalystTeam.get_analyst_prompt(analyst)
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
            console.print("\n[bold yellow]═══ TIER 2: SENIOR MANAGER ═══[/bold yellow]")
            progress.update(task, description="[cyan]Senior Manager synthesizing reports...")
            
            senior_data = {"data": junior_reports}
            senior_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.senior_model,
                self.senior_temp
            )
            senior_report = await senior_analyzer.analyze_async(
                self.SENIOR_SYNTHESIS_PROMPT, senior_data
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] Senior Manager synthesis complete")
            
            # TIER 3: Executive Committee Final Review
            console.print("\n[bold yellow]═══ TIER 3: EXECUTIVE COMMITTEE ═══[/bold yellow]")
            progress.update(task, description="[cyan]Executive Committee deliberating...")
            
            executive_data = {"data": {"senior_report": senior_report, "analyst_count": len(junior_reports)}}
            executive_analyzer = OllamaAnalyzer(
                self.ollama_base_url,
                self.executive_model,
                self.executive_temp
            )
            final_decision = await executive_analyzer.analyze_async(
                self.EXECUTIVE_COMMITTEE_PROMPT, executive_data
            )
            progress.advance(task)
            console.print(f"[green]✓[/green] Executive Committee decision complete\n")
        
        return final_decision
    
    async def _run_junior_analyst(self, analyst: AnalystProfile, analyzer: OllamaAnalyzer, 
                                   prompt: str, data: Dict[str, Any]) -> tuple:
        """Run a single junior analyst analysis asynchronously."""
        result = await analyzer.analyze_async(prompt, data)
        return (analyst.name, analyst.role, analyst.focus_area, result)
