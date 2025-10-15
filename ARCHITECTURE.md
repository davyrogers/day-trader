# Architecture Overview

## System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Day Trader Workflow                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Schedule   │  (Optional - hourly trigger)
│   Trigger    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STEP 1: RSS Feed Fetching                     │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  FXStreet   │  │ InvestingLive│  │ DailyForex  │  + 5 more   │
│  │    News     │  │              │  │   4 feeds   │             │
│  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘             │
│         │                │                  │                     │
│         └────────────────┴──────────────────┘                     │
│                          │                                        │
│                          ▼                                        │
│                  [ Merge & Aggregate ]                            │
│                    ~200-400 articles                              │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                  STEP 2: AI Analysis Pipeline                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Agent 1: DeepSeek R1 8B                                │    │
│  │  Prompt: Analyze for EUR/USD shorting opportunities     │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Agent 2: GPT-OSS 20B                                   │    │
│  │  Prompt: Analyze for EUR/USD shorting opportunities     │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Agent 3: GPT-OSS 20B                                   │    │
│  │  Prompt: Analyze for EUR/USD shorting opportunities     │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Agent 4: GPT-OSS 20B                                   │    │
│  │  Prompt: Analyze for EUR/USD shorting opportunities     │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│                  [ Collect All Analyses ]                        │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Synthesis Agent: GPT-OSS 20B                           │    │
│  │  Prompt: Combine all analyses into actionable advice    │    │
│  │  - Risk/reward calculation                              │    │
│  │  - £100 investment examples                             │    │
│  │  - Time-sensitive alerts                                │    │
│  │  - BLUF format (Bottom Line Up Front)                   │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                                                                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                  STEP 3: Discord Notification                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Discord Webhook                                        │    │
│  │  - Truncate to 2000 chars if needed                     │    │
│  │  - Send synthesized analysis                            │    │
│  │  - Fallback to console if no webhook                    │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                           │
                           ▼
                    [ Complete ] ✓


## Component Architecture

┌──────────────────────────────────────────────────────────────────┐
│                         main.py                                  │
│                   (Workflow Orchestrator)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐         │
│  │   config    │  │ rss_fetcher  │  │  ai_analyzer   │         │
│  │             │  │              │  │                │         │
│  │ - Settings  │  │ - RSSFeed    │  │ - OllamaAnalyzer│        │
│  │ - Env vars  │  │ - Aggregator │  │ - Pipeline     │         │
│  └─────────────┘  └──────────────┘  └────────────────┘         │
│                                                                   │
│  ┌─────────────────┐                                             │
│  │ discord_sender  │                                             │
│  │                 │                                             │
│  │ - Webhook       │                                             │
│  │ - Fallback      │                                             │
│  └─────────────────┘                                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘


## Data Flow

┌────────────┐
│  Raw RSS   │  JSON entries with title, content, date, etc.
│   Feeds    │
└─────┬──────┘
      │
      ▼
┌────────────────┐
│   Aggregated   │  { "data": [ {...}, {...}, ... ] }
│     Data       │  ~200-400 articles
└────────┬───────┘
         │
         ▼
┌──────────────────┐
│  AI Analysis 1-4 │  Individual agent perspectives
│                  │  Focus: EUR/USD shorts, volatility times
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Synthesis      │  Combined analysis with:
│                  │  - Risk/reward
│                  │  - Timing
│                  │  - Actionable advice
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Discord        │  <= 2000 chars, BLUF format
│   Message        │
└──────────────────┘


## Technology Stack

┌─────────────────────────────────────────────────────────────────┐
│  Core Technologies                                              │
├─────────────────────────────────────────────────────────────────┤
│  • Python 3.9+                                                  │
│  • Rich (CLI interface)                                         │
│  • Pydantic (configuration)                                     │
│  • HTTPX (async HTTP)                                           │
├─────────────────────────────────────────────────────────────────┤
│  Data Sources                                                   │
├─────────────────────────────────────────────────────────────────┤
│  • FeedParser (RSS)                                             │
│  • 8 forex news RSS feeds                                       │
├─────────────────────────────────────────────────────────────────┤
│  AI/ML                                                          │
├─────────────────────────────────────────────────────────────────┤
│  • Ollama (local LLM server)                                    │
│  • GPT-OSS 20B (3 agents)                                       │
│  • DeepSeek R1 8B (1 agent)                                     │
├─────────────────────────────────────────────────────────────────┤
│  Integrations                                                   │
├─────────────────────────────────────────────────────────────────┤
│  • Discord Webhooks                                             │
│  • Schedule (optional automation)                               │
└─────────────────────────────────────────────────────────────────┘


## Execution Modes

### Mode 1: One-Time Execution
```
python run.py  →  Fetch → Analyze → Send → Done ✓
```

### Mode 2: Scheduled Execution
```
python run.py  →  [Fetch → Analyze → Send] → Wait 1hr → Repeat ∞
                  Press Ctrl+C to stop
```


## Error Handling

Each component has robust error handling:

```
RSS Fetcher
  ├─ Individual feed failure → Log warning, continue with others
  └─ All feeds fail → Exit with error

AI Analyzer
  ├─ Single agent failure → Log error, continue with others
  ├─ Model not found → Clear error message
  └─ Ollama not running → Connection error with fix suggestion

Discord Sender
  ├─ No webhook URL → Print to console instead
  ├─ Message too long → Auto-truncate to 2000 chars
  └─ Webhook invalid → HTTP error with details
```


## Performance Characteristics

• RSS Fetching: ~5-10 seconds (parallel requests)
• AI Analysis: ~2-5 minutes (4 agents + synthesis)
• Discord Send: < 1 second
• Total: ~3-6 minutes per run

Memory usage: ~200-500 MB
CPU usage: High during AI analysis, low otherwise


## Scalability Notes

Current design processes:
• 8 RSS feeds
• ~200-400 articles per run
• 4 AI agents + 1 synthesis

To scale:
• Add more RSS feeds to `rss_fetcher.py`
• Adjust agent count in `ai_analyzer.py`
• Use smaller models for faster analysis
• Implement caching to avoid re-analyzing articles
