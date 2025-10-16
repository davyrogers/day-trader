# System Flow Visualization

## Complete Information Pipeline

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                          DATA COLLECTION LAYER                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    103 RSS FEEDS (Rate-Limited, Concurrent Fetching)
    ├─ FXStreet (4 feeds)
    ├─ DailyForex (5 feeds)
    ├─ Investing.com (7 feeds)
    ├─ ForexLive (2 feeds)
    ├─ Reuters (2 feeds)
    ├─ MarketWatch (4 feeds)
    ├─ Financial Times (4 feeds)
    ├─ Major Brokers (30+ feeds: OANDA, FXCM, IG, etc.)
    ├─ Economic Blogs (5 feeds: Mish Talk, Wolf Street, etc.)
    └─ Alternative News (40+ feeds)

    ⚙️  Rate Limiting: Max 10 concurrent | 0.1-0.3s delays
    ⏱️  Fetch Time: ~30-60 seconds
    📊 Typical Yield: 500-2000 articles

                                ⬇️

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    TIER 1: JUNIOR ANALYST REVIEW                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
    │ 🛡️ MARCUS      │  │ 📊 SARAH       │  │ 🚀 JAMES       │
    │ Risk Mgmt      │  │ Technical      │  │ Momentum       │
    │ llama3.2:0.3   │  │ qwen2.5:0.5    │  │ mistral:0.8    │
    │                │  │                │  │                │
    │ LOOKS FOR:     │  │ LOOKS FOR:     │  │ LOOKS FOR:     │
    │ • Risks        │  │ • Patterns     │  │ • Breakouts    │
    │ • Warnings     │  │ • Levels       │  │ • Momentum     │
    │ • Stop losses  │  │ • Timing       │  │ • Conviction   │
    └────────────────┘  └────────────────┘  └────────────────┘

    ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
    │ 🌍 ELENA       │  │ 🔄 DAVID       │  │ 💭 PRIYA       │
    │ Fundamental    │  │ Contrarian     │  │ Sentiment      │
    │ llama3.2:0.4   │  │ gemma2:0.7     │  │ phi3:0.6       │
    │                │  │                │  │                │
    │ LOOKS FOR:     │  │ LOOKS FOR:     │  │ LOOKS FOR:     │
    │ • Econ data    │  │ • Consensus    │  │ • Fear/Greed   │
    │ • CB policy    │  │ • Traps        │  │ • Positioning  │
    │ • Geopolitics  │  │ • Alternatives │  │ • Mood shifts  │
    └────────────────┘  └────────────────┘  └────────────────┘

    Each analyst independently reviews ALL news from their perspective
    
    ⏱️  Time: 2-5 min per analyst (concurrent) or 12-30 min (sequential)
    📝 Output: 6 independent reports with timing, risks, opportunities

                                ⬇️

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    TIER 2: SENIOR MANAGER SYNTHESIS                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                        ┌─────────────────────┐
                        │  👔 SENIOR MANAGER  │
                        │  llama3.2:0.4       │
                        │                     │
                        │  RESPONSIBILITIES:  │
                        │  • Synthesize       │
                        │  • Find consensus   │
                        │  • Flag conflicts   │
                        │  • Filter noise     │
                        │  • Consolidate time │
                        └─────────────────────┘

    Receives all 6 analyst reports and creates unified view:
    
    ✅ CONSENSUS ITEMS
       - Points where 3+ analysts agree
       - Common timing windows identified
       - Shared risk concerns
    
    ⚠️ DISAGREEMENTS
       - Where analysts diverge
       - Reasoning for different views
       - Risk vs opportunity trade-offs
    
    🎯 CONSOLIDATED OUTLOOK
       - Key events with exact times
       - Market direction consensus
       - Trade opportunity assessment

    ⏱️  Time: 2-3 minutes
    📝 Output: Synthesized management report

                                ⬇️

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                  TIER 3: EXECUTIVE COMMITTEE DECISION                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                    ┌───────────────────────────┐
                    │  🎩 EXECUTIVE COMMITTEE   │
                    │  llama3.2:0.3             │
                    │                           │
                    │  FINAL DECISION MAKERS:   │
                    │  • Debate trade merits    │
                    │  • Verify calculations    │
                    │  • Build consensus        │
                    │  • Approve/reject trades  │
                    │  • Issue clear guidance   │
                    └───────────────────────────┘

    DECISION PROCESS:
    
    1️⃣  Review senior manager's consolidated report
    2️⃣  Debate among committee members (simulated)
    3️⃣  Verify all timing and risk/reward math
    4️⃣  Check for remaining noise or uncertainty
    5️⃣  Build final consensus on recommendation
    6️⃣  Format for Discord (BLUF, under 1500 chars)

    OUTPUT INCLUDES:
    ━━━━━━━━━━━━━━━━━━━━
    🎯 Clear YES/NO/WATCH decision
    ⏰ 2-3 critical time windows (UTC)
    💹 Specific trade setup (if applicable)
       • Pair, direction, timing
       • Risk/reward in £ on £100
       • Probability with reasoning
    ⚠️ Top 2-3 risks
    🎲 Final recommendation (2-3 sentences)
    ━━━━━━━━━━━━━━━━━━━━

    ⏱️  Time: 2-3 minutes
    📝 Output: Actionable trading signal

                                ⬇️

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            DISCORD DELIVERY                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                        📱 Discord Webhook
                    Clear, actionable message
                    Formatted for mobile reading
                    All acronyms explained
                    Risk/reward in plain terms
                    Specific timing windows
                    
                    ⏱️  Delivery: Instant
```

## Information Filtering at Each Stage

```
Stage           Input Size       Processing              Output Size
─────────────────────────────────────────────────────────────────────
RSS Feeds       500-2000        Rate-limited fetch      500-2000
                articles        (103 feeds)             articles

Junior          500-2000        6 independent           6 reports
Analysts        articles        analyses                (~2-3 pages each)

Senior          6 reports       Synthesis &             1 report
Manager         (~12-18 pages)  consolidation           (~2-3 pages)

Executive       1 report        Verification &          1 signal
Committee       (~2-3 pages)    decision                (~300-500 words)

Discord         1 signal        Formatting              1 message
                (~500 words)    & delivery              (<1500 chars)
```

## Noise Reduction Through Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  NOISE LEVEL: ████████████████████████████████ 100%         │
│  (Raw RSS: 500-2000 articles, many irrelevant)              │
└─────────────────────────────────────────────────────────────┘
                            ⬇️
┌─────────────────────────────────────────────────────────────┐
│  NOISE LEVEL: ████████████████░░░░ 60%                      │
│  (6 analysts filter their perspective)                      │
└─────────────────────────────────────────────────────────────┘
                            ⬇️
┌─────────────────────────────────────────────────────────────┐
│  NOISE LEVEL: ████████░░░░░░░░ 30%                          │
│  (Senior manager consolidates & removes conflicts)          │
└─────────────────────────────────────────────────────────────┘
                            ⬇️
┌─────────────────────────────────────────────────────────────┐
│  NOISE LEVEL: ██░░░░░░░░░░░░░░ 5%                           │
│  (Executive committee final verification)                   │
└─────────────────────────────────────────────────────────────┘
                            ⬇️
┌─────────────────────────────────────────────────────────────┐
│  SIGNAL: Clear, actionable, specific trade recommendation   │
└─────────────────────────────────────────────────────────────┘
```

## Total Processing Time

| Mode       | RSS Fetch | Tier 1  | Tier 2 | Tier 3 | Total    |
|------------|-----------|---------|--------|--------|----------|
| Concurrent | 30-60s    | 2-5 min | 2-3 min| 2-3 min| 10-15min |
| Sequential | 30-60s    | 12-30min| 2-3 min| 2-3 min| 20-40min |

**Recommendation**: Use concurrent mode if your hardware can handle it (16GB+ RAM, modern CPU)
