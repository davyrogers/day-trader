# Quick Reference Guide - Enhanced Analyst Team v2.0

## What Changed?

### Team Size
- **Before**: 6 analysts + 2 management layers = 8 total
- **Now**: 15 analysts + 7 management layers = 22 total

### New Analysts by Category

#### Sentiment Analysts (3 new)
1. **Rachel** - Retail sentiment (contrarian to retail positioning)
2. **Wei** - Institutional flow (smart money tracking)
3. **Aisha** - Market psychology (behavioral finance)

#### Fundamental Analysts (5 new)
1. **Henrik** - Monetary policy (central bank expert)
2. **Sofia** - Trade balance (current account specialist)
3. **Dmitri** - Inflation (CPI/PPI dynamics)
4. **Yuki** - Employment (labor market data)
5. **Pierre** - GDP growth (economic growth indicators)
6. **Isabella** - Geopolitics (political risk assessment)

#### Risk Analyst (1 new) - THE DEVIL'S ADVOCATE
**Viktor** - Chief Risk Officer who ONLY looks for problems:
- Questions all trade ideas
- Identifies traps and false signals
- Points out hidden risks
- Challenges optimistic assumptions
- **This is your "reality check" analyst**

### New Management Layers

#### 4 Senior Managers (different risk appetites)
1. **Alpha** (Conservative) - Temp 0.25 - Strictest validation
2. **Beta** (Balanced) - Temp 0.35 - Balanced approach
3. **Gamma** (Aggressive) - Temp 0.45 - Seeks opportunities
4. **Delta** (Precision) - Temp 0.30 - Analytical rigor

#### 3 Executive Committees (multiple perspectives)
1. **Prime** (Ultra-Conservative) - Temp 0.20 - Highest standards
2. **Alpha** (Balanced) - Temp 0.30 - Clear R:R focus
3. **Omega** (Opportunistic) - Temp 0.35 - High-probability setups

## Key Features

### ✅ Evidence-Based Reasoning
Every analyst MUST provide:
- Specific evidence for conclusions
- Citations of news items and data
- No speculation or made-up facts
- Clear reasoning from evidence to recommendation

### ✅ Real-Time Market Data
Management layers now receive:
- Current EUR/USD price
- Bid/Ask spread
- Live market data from multiple sources
- Validates recommendations against actual prices

### ✅ Multiple Perspectives
You get 3 different executive decisions:
- Conservative view (Committee Prime)
- Balanced view (Committee Alpha)
- Opportunistic view (Committee Omega)

**Choose the committee that matches your risk appetite!**

## How to Use

### 1. Run Analysis (No Code Changes Needed)
```bash
python run.py
```

The system automatically:
- Fetches real-time market data
- Runs all 15 analysts
- Synthesizes via 4 managers
- Provides 3 executive decisions

### 2. Read the Output

#### Look for:
- **Viktor's Analysis** - What could go wrong?
- **Market Data Section** - Current EUR/USD price
- **Manager Synthesis** - How do 4 managers see it?
- **3 Executive Decisions** - Choose your preferred risk level

### 3. Choose Your Committee

- **Risk-Averse?** → Follow Committee Prime (Ultra-Conservative)
- **Balanced Trader?** → Follow Committee Alpha (Balanced)
- **Aggressive Trader?** → Follow Committee Omega (Opportunistic)

## Configuration

### analyst_team.json
All configuration is in this file:
- 15 junior analysts
- 4 senior managers
- 3 executive committees
- Each with specific personality and temperature

### Modify Temperature
Lower = More conservative, higher = More creative

```json
{
  "temperature": 0.3  // Range: 0.0 - 1.0
}
```

### Add/Remove Analysts
Edit the `junior_analysts` array in `analyst_team.json`

## Market Data

### Automatic Data Sources
The system tries these APIs in order:
1. exchangerate-api.com (free, no key)
2. frankfurter.app (free ECB data)
3. fixer.io (requires API key)

### Add API Key (Optional)
In `src/config.py` or environment variable:
```python
MARKET_DATA_API_KEY=your_key_here
```

### Fallback Behavior
If all APIs fail, the system continues but warns managers that real-time data is unavailable.

## Understanding Viktor (Devil's Advocate)

Viktor is your **risk protection**:
- Skeptical of everything
- Looks for reasons NOT to trade
- Identifies hidden risks
- Questions consensus

**Don't ignore Viktor!** If he raises serious concerns, listen.

## Temperature Guide

### Junior Analysts
- **0.3-0.4** - Very conservative (Risk, Fundamental analysts)
- **0.5-0.6** - Balanced (Technical, Sentiment)
- **0.7-0.8** - Creative/Contrarian (James, David)

### Senior Managers
- **0.25-0.30** - Conservative synthesis
- **0.35-0.45** - Balanced to aggressive synthesis

### Executive Committees
- **0.20** - Ultra-conservative decisions
- **0.30** - Balanced decisions
- **0.35** - Opportunistic decisions

## Expected Output Format

```
================================================================================
FINAL EXECUTIVE DECISIONS
================================================================================

────────────────────────────────────────────────────────────────────────────────
Executive Committee Prime (Executive Decision Makers - Ultra-Conservative)
────────────────────────────────────────────────────────────────────────────────

🎯 TRADING SIGNAL - [DATE]
━━━━━━━━━━━━━━━━━━━━
📊 CONSENSUS: [Yes/No/Watch]
💱 CURRENT MARKET (EUR/USD):
Price: 1.16371
Bid/Ask: 1.16359 / 1.16382
... [rest of decision]

────────────────────────────────────────────────────────────────────────────────
Executive Committee Alpha (Executive Decision Makers - Balanced)
────────────────────────────────────────────────────────────────────────────────

[Similar format with different perspective]

────────────────────────────────────────────────────────────────────────────────
Executive Committee Omega (Executive Decision Makers - Opportunistic)
────────────────────────────────────────────────────────────────────────────────

[Similar format with different perspective]
```

## Troubleshooting

### Market Data Not Loading
- Check internet connection
- Verify no firewall blocking API calls
- System will continue with warning

### Too Many Analysts Taking Too Long
- Use concurrent mode (default in run.py)
- Ensure Ollama models are loaded
- Consider reducing analyst count in config

### Analysts Giving Generic Advice
- Verify `evidence-based reasoning` requirement in prompts
- Check that news data is rich and specific
- May need to adjust analyst prompts

## Performance Tips

### Concurrent Mode (Recommended)
All analysts run in parallel = much faster
```python
run_concurrent=True  # Default
```

### Sequential Mode (Slower but more stable)
Analysts run one at a time
```python
run_concurrent=False
```

### Memory Management
Ollama models are unloaded after each request to prevent context mixing

## What to Expect

### Analysis Time
- **Concurrent**: ~5-10 minutes (15 analysts + 4 managers + 3 committees in parallel)
- **Sequential**: ~20-30 minutes (all run one by one)

### Quality Improvements
- More comprehensive coverage
- Better risk assessment (thanks to Viktor)
- Real price validation
- Multiple decision perspectives

### Decision Making
You now get 3 opinions from different risk profiles:
1. Conservative committee - rarely trades, high confidence only
2. Balanced committee - moderate risk/reward
3. Opportunistic committee - more willing to take quality setups

**Choose based on your risk tolerance!**

## Summary

✅ **15 Analysts** covering all aspects of forex analysis  
✅ **Viktor** as devil's advocate for risk protection  
✅ **4 Senior Managers** with different perspectives  
✅ **3 Executive Committees** for multiple decision views  
✅ **Real-Time Market Data** for price validation  
✅ **Evidence-Based** reasoning required from all analysts  
✅ **No Code Changes Needed** - just run `python run.py`

## Questions?

See full documentation in:
- `ENHANCEMENT_V2_SUMMARY.md` - Detailed technical changes
- `analyst_team.json` - Full configuration
- `src/market_data.py` - Market data implementation
- `src/ai_analyzer.py` - Enhanced analysis pipeline
