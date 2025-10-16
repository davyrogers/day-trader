# Three-Tier AI Analysis Pipeline

## Overview
This system implements a hierarchical information pipeline with multiple layers of AI analysis to convert raw forex news into actionable trading decisions.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    103 RSS FEEDS                             │
│  (FXStreet, DailyForex, Reuters, Bloomberg, etc.)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              TIER 1: JUNIOR ANALYSTS (6)                     │
│  Each with unique personality, focus area, and temperature   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Marcus (Conservative) - Risk Management                  │
│     Model: llama3.2 | Temp: 0.3 | Focus: Capital protection │
│                                                              │
│  2. Sarah (Technical) - Technical Analysis                   │
│     Model: qwen2.5 | Temp: 0.5 | Focus: Chart patterns      │
│                                                              │
│  3. James (Aggressive) - Momentum Trading                    │
│     Model: mistral | Temp: 0.8 | Focus: Breakouts          │
│                                                              │
│  4. Elena (Fundamental) - Economic Policy                    │
│     Model: llama3.2 | Temp: 0.4 | Focus: Macro economics   │
│                                                              │
│  5. David (Contrarian) - Contrarian Strategy                 │
│     Model: gemma2 | Temp: 0.7 | Focus: Contrary indicators │
│                                                              │
│  6. Priya (Sentiment) - Market Sentiment                     │
│     Model: phi3 | Temp: 0.6 | Focus: Fear/greed indicators │
│                                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           TIER 2: SENIOR MANAGER                             │
│  Synthesizes 6 analyst reports into coherent picture         │
├─────────────────────────────────────────────────────────────┤
│  • Identifies consensus and disagreements                    │
│  • Filters out noise and conflicting signals                 │
│  • Consolidates time-specific opportunities                  │
│  • Notes divergent views with explanations                   │
│                                                              │
│  Model: llama3.2 | Temp: 0.4 (Balanced)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        TIER 3: EXECUTIVE COMMITTEE                           │
│  Final decision layer - makes actionable recommendations     │
├─────────────────────────────────────────────────────────────┤
│  • Debates merits of proposed trades                         │
│  • Verifies timing and risk/reward calculations             │
│  • Filters remaining noise                                   │
│  • Builds consensus on specific recommendations             │
│  • Provides clear, actionable guidance                       │
│                                                              │
│  Model: llama3.2 | Temp: 0.3 (Very conservative)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  DISCORD OUTPUT                              │
│  Clear, actionable trading signal with specific timing       │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Diverse Perspectives (Tier 1)
- **6 distinct analyst personalities** provide different viewpoints
- **Different AI models** for variety in analysis approach
- **Temperature variation** (0.3-0.8) for conservative to creative thinking
- **Specialized focus areas** ensure comprehensive coverage

### 2. Information Synthesis (Tier 2)
- Senior manager **consolidates** junior analyst reports
- **Identifies consensus** where multiple analysts agree
- **Flags disagreements** and explains reasoning
- **Filters noise** before passing to executive level

### 3. Executive Decision-Making (Tier 3)
- **Management debate** simulates real trading desk deliberation
- **Verification layer** checks timing and risk calculations
- **Final consensus building** on actionable trades
- **BLUF format** output optimized for Discord

## Trading Focus

**Primary Strategy**: EUR/USD shorting opportunities
- Trade WITH major trends (never against the market)
- News-driven entry timing
- Small, lower-risk profit opportunities
- Un-leveraged positions (£100 base calculations)

## Output Format

The final Discord message includes:
- **Consensus** on trade opportunity (Yes/No/Watch)
- **Key Times** in UTC for critical events (2-3 only)
- **Trade Setup** with specific entry timing
- **Risk/Reward** in actual £ amounts on £100 position
- **Probability/Odds** with clear reasoning
- **Top Risks** (2-3 maximum)
- **Executive Decision** (clear 2-3 sentence recommendation)

## Benefits

1. **Noise Reduction**: Multiple filtering layers remove irrelevant information
2. **Bias Mitigation**: Diverse perspectives catch blind spots
3. **Consensus Building**: Multiple analysts must agree for high-confidence signals
4. **Risk Management**: Conservative overlay at senior/executive levels
5. **Actionable Output**: Clear, specific recommendations with timing
6. **Beginner-Friendly**: All acronyms explained, risk/reward in plain terms

## Configuration

The analyst team is **hardcoded** for consistency and reliability. To modify:
- Edit `AIAnalystTeam.ANALYSTS` in `ai_analyzer.py`
- Adjust models, temperatures, or personality descriptions
- Add/remove analysts as needed

**Concurrent vs Sequential Mode**:
- Set `RUN_CONCURRENT=true` in `.env` for faster execution
- Set `RUN_CONCURRENT=false` if Ollama can't handle parallel requests
- Sequential mode runs analysts one-by-one but takes longer
