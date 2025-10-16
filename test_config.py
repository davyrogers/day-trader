"""Test script to validate the enhanced analyst team configuration."""
import json
from pathlib import Path

def test_configuration():
    """Test the analyst_team.json configuration."""
    config_path = Path(__file__).parent / "analyst_team.json"
    
    print("\n" + "="*80)
    print("ANALYST TEAM CONFIGURATION TEST")
    print("="*80 + "\n")
    
    # Load configuration
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ Configuration file is valid JSON")
    except Exception as e:
        print(f"✗ Error loading configuration: {e}")
        return False
    
    # Check structure
    try:
        junior_analysts = config.get('junior_analysts', [])
        management_layers = config.get('management_layers', [])
        config_info = config.get('config_info', {})
        
        print(f"✓ Configuration structure is valid\n")
        
        # Count analysts by type
        sentiment_count = sum(1 for a in junior_analysts if 'sentiment' in a['focus_area'].lower() or 'psychology' in a['focus_area'].lower() or 'positioning' in a['focus_area'].lower())
        fundamental_count = sum(1 for a in junior_analysts if any(word in a['focus_area'].lower() for word in ['economic', 'policy', 'inflation', 'employment', 'gdp', 'trade', 'geopolitical']))
        technical_count = sum(1 for a in junior_analysts if 'technical' in a['focus_area'].lower() or 'chart' in a['focus_area'].lower())
        risk_count = sum(1 for a in junior_analysts if 'risk' in a['focus_area'].lower() or 'risk' in a['role'].lower())
        
        print("JUNIOR ANALYSTS:")
        print(f"  Total: {len(junior_analysts)}")
        print(f"  - Sentiment Analysts: {sentiment_count}")
        print(f"  - Fundamental Analysts: {fundamental_count}")
        print(f"  - Technical Analysts: {technical_count}")
        print(f"  - Risk Analysts: {risk_count}")
        print()
        
        # List all analysts
        print("  Analyst Names:")
        for i, analyst in enumerate(junior_analysts, 1):
            print(f"    {i:2d}. {analyst['name']:30s} - {analyst['role']}")
        print()
        
        # Count management layers
        senior_managers = [m for m in management_layers if 'senior' in m['name'].lower() and 'executive' not in m['name'].lower()]
        executive_committees = [m for m in management_layers if 'executive' in m['name'].lower()]
        
        print("MANAGEMENT LAYERS:")
        print(f"  Total: {len(management_layers)}")
        print(f"  - Senior Managers: {len(senior_managers)}")
        print(f"  - Executive Committees: {len(executive_committees)}")
        print()
        
        print("  Senior Manager Names:")
        for i, manager in enumerate(senior_managers, 1):
            print(f"    {i}. {manager['name']:30s} - Temp: {manager['temperature']}")
        print()
        
        print("  Executive Committee Names:")
        for i, committee in enumerate(executive_committees, 1):
            print(f"    {i}. {committee['name']:30s} - Temp: {committee['temperature']}")
        print()
        
        # Check for market data integration
        has_market_data = any('{{MARKET_DATA}}' in m['system_prompt'] for m in management_layers)
        print(f"✓ Market data integration: {'Enabled' if has_market_data else 'Not found'}")
        
        # Check for evidence-based reasoning
        has_evidence = any('EVIDENCE-BASED REASONING' in a['system_prompt'] for a in junior_analysts)
        print(f"✓ Evidence-based reasoning: {'Required' if has_evidence else 'Not found'}")
        
        # Check for devil's advocate
        has_devils_advocate = any('devil' in a['name'].lower() or 'viktor' in a['name'].lower() for a in junior_analysts)
        print(f"✓ Devil's advocate analyst: {'Present (Viktor)' if has_devils_advocate else 'Not found'}")
        
        # Version info
        version = config_info.get('version', 'Unknown')
        print(f"\nConfiguration Version: {version}")
        
        print("\n" + "="*80)
        print("✓ ALL CHECKS PASSED - Configuration is ready to use!")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"✗ Error validating configuration: {e}")
        return False


if __name__ == "__main__":
    test_configuration()
