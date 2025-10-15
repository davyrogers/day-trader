#!/usr/bin/env python
"""Setup verification script to check all dependencies and configuration."""
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (requires 3.9+)"


def check_packages():
    """Check if required packages are installed."""
    packages = [
        "feedparser",
        "ollama",
        "httpx",
        "rich",
        "pydantic",
        "pydantic_settings",
        "dotenv",
        "schedule",
    ]
    
    results = []
    for package in packages:
        try:
            __import__(package)
            results.append((package, True, "Installed"))
        except ImportError:
            results.append((package, False, "Missing"))
    
    return results


def check_ollama():
    """Check if Ollama is accessible."""
    try:
        import httpx
        client = httpx.Client(timeout=5.0)
        response = client.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        models = [model["name"] for model in data.get("models", [])]
        client.close()
        return True, models
    except Exception as e:
        return False, str(e)


def check_env_file():
    """Check if .env file exists."""
    return os.path.exists(".env"), ".env file exists" if os.path.exists(".env") else ".env file missing"


def check_required_models():
    """Check if required Ollama models are installed."""
    required = ["gpt-oss:20b", "deepseek-r1:8b"]
    ollama_ok, models = check_ollama()
    
    if not ollama_ok:
        return False, required, []
    
    installed = [m for m in required if any(m in model for model in models)]
    missing = [m for m in required if m not in installed]
    
    return len(missing) == 0, required, installed


def main():
    """Run all checks and display results."""
    console.print(Panel.fit(
        "[bold cyan]Day Trader Setup Verification[/bold cyan]",
        border_style="cyan"
    ))
    
    # Results table
    table = Table(title="System Check", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", width=30)
    table.add_column("Status", width=15)
    table.add_column("Details", style="dim")
    
    # Python version
    py_ok, py_version = check_python_version()
    table.add_row(
        "Python Version",
        "[green]✓[/green]" if py_ok else "[red]✗[/red]",
        py_version
    )
    
    # Packages
    package_results = check_packages()
    all_packages_ok = all(ok for _, ok, _ in package_results)
    missing_packages = [pkg for pkg, ok, _ in package_results if not ok]
    
    table.add_row(
        "Python Packages",
        "[green]✓[/green]" if all_packages_ok else "[red]✗[/red]",
        f"{sum(1 for _, ok, _ in package_results if ok)}/{len(package_results)} installed"
    )
    
    # Ollama
    ollama_ok, ollama_info = check_ollama()
    table.add_row(
        "Ollama Service",
        "[green]✓[/green]" if ollama_ok else "[red]✗[/red]",
        f"{len(ollama_info)} models available" if ollama_ok else f"Error: {ollama_info}"
    )
    
    # Required models
    models_ok, required, installed = check_required_models()
    table.add_row(
        "Required Models",
        "[green]✓[/green]" if models_ok else "[red]✗[/red]",
        f"{len(installed)}/{len(required)} installed"
    )
    
    # .env file
    env_ok, env_msg = check_env_file()
    table.add_row(
        "Configuration",
        "[green]✓[/green]" if env_ok else "[yellow]⚠[/yellow]",
        env_msg
    )
    
    console.print(table)
    console.print()
    
    # Detailed feedback
    all_ok = py_ok and all_packages_ok and ollama_ok and models_ok
    
    if not all_ok:
        console.print("[bold red]Issues Found:[/bold red]\n")
        
        if not py_ok:
            console.print("❌ Python version too old. Please upgrade to Python 3.9 or newer.")
        
        if not all_packages_ok:
            console.print(f"❌ Missing packages: {', '.join(missing_packages)}")
            console.print("   Fix: pip install -r requirements.txt\n")
        
        if not ollama_ok:
            console.print("❌ Ollama service not accessible")
            console.print("   Fix: Make sure Ollama is installed and running (ollama serve)\n")
        
        if not models_ok:
            missing = [m for m in required if m not in installed]
            console.print(f"❌ Missing Ollama models: {', '.join(missing)}")
            for model in missing:
                console.print(f"   Fix: ollama pull {model}")
            console.print()
        
        if not env_ok:
            console.print("⚠️  .env file not found")
            console.print("   Fix: copy .env.example .env")
            console.print("   Then edit .env to add your Discord webhook URL\n")
    else:
        console.print(Panel.fit(
            "[bold green]✓ All checks passed! You're ready to run the workflow.[/bold green]\n\n"
            "Run: [cyan]python run.py[/cyan]",
            border_style="green"
        ))
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
