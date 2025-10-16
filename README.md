# Forex News Squawk Analyzer

A sophisticated Python-based workflow that analyzes forex news through a **three-tier AI hierarchy** to generate actionable trading signals.

## 🎯 What This Does

Imagine a **professional trading desk** with:
- 👥 **6 Junior Analysts** (each with unique personality and expertise)
- 👔 **1 Senior Manager** (synthesizes analyst reports)
- 🎩 **Executive Committee** (makes final trading decisions)

This system fetches news from **103 forex sources**, processes it through this AI hierarchy, and delivers **clear, actionable recommendations** to Discord.

## ✨ Key Features

- 📡 **103 RSS Feeds** from major forex news sources (FXStreet, DailyForex, Reuters, Bloomberg, etc.)
- 🚦 **Rate Limiting** to prevent getting blocked by news sources
- 🤖 **6 AI Analyst Personalities** with different models, temperatures, and focus areas:
  - Marcus (Conservative Risk Manager)
  - Sarah (Technical Analyst)
  - James (Aggressive Momentum Trader)
  - Elena (Fundamental Economist)
  - David (Contrarian Strategist)
  - Priya (Sentiment Analyst)
- 🏢 **3-Tier Analysis Pipeline**:
  - Tier 1: Junior analysts review raw news
  - Tier 2: Senior manager synthesizes reports
  - Tier 3: Executive committee makes final decision
- 📝 **Complete Report Saving** - All AI decisions automatically saved to `reports/` folder for review
- 💬 **Discord Integration** with clear BLUF format output
- 📊 **Rich CLI** with progress indicators
- ⚡ **Concurrent or Sequential** execution modes
- ⏰ **Scheduled or One-Time** execution

## 📋 Prerequisites

1. **Python 3.9+** installed
2. **Ollama** installed and running locally with these models:
   ```bash
   ollama pull llama3.2:latest
   ollama pull qwen2.5:latest
   ollama pull mistral:latest
   ollama pull gemma2:latest
   ollama pull phi3:latest
   ```

3. **Discord Webhook URL** (optional, for receiving signals)

## 🚀 Quick Start

1. Clone the repository (if not already done):
   ```bash
   git clone <your-repo-url>
   cd day-trader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### Windows (Recommended)

1. **Run the installer**:
   ```bash
   install.bat
   ```
   This installs all dependencies and verifies your setup.

2. **Configure your environment**:
   Edit `.env` file with your Discord webhook:
   ```
   DISCORD_WEBHOOK_URL=your_webhook_url_here
   RUN_CONCURRENT=false
   ```

3. **Run the analyzer**:
   ```bash
   start.bat
   ```

### Manual Installation

1. Clone and install:
   ```bash
   git clone <your-repo-url>
   cd day-trader
   pip install -r requirements.txt
   ```

2. Create `.env` file:
   ```bash
   copy .env.example .env
   ```

3. Configure your Discord webhook URL in `.env`

4. Run:
   ```bash
   python run.py
   ```

## 📖 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - ⚡ Quick reference card for daily use
- **[ANALYST_CONFIG.md](ANALYST_CONFIG.md)** - 🔧 Configure your analyst team (JSON-based)
- **[REPORTS_QUICK_REFERENCE.md](REPORTS_QUICK_REFERENCE.md)** - 📝 How to review saved AI reports
- **[REPORT_SAVING_FEATURE.md](REPORT_SAVING_FEATURE.md)** - 📄 Report saving feature documentation
- **[REPORTS_STRUCTURE_EXAMPLE.md](REPORTS_STRUCTURE_EXAMPLE.md)** - 📁 Example of reports folder structure
- **[ANALYSIS_PIPELINE.md](ANALYSIS_PIPELINE.md)** - Detailed architecture of the 3-tier AI system
- **[ANALYST_TEAM.md](ANALYST_TEAM.md)** - Meet the 6 AI analysts and their personalities
- **[SYSTEM_FLOW.md](SYSTEM_FLOW.md)** - Visual pipeline and information flow
- **[EXAMPLE_OUTPUTS.md](EXAMPLE_OUTPUTS.md)** - See real examples from each tier
- **[ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md)** - What's new in this version
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
- **[CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)** - All configuration options
- **[PERFORMANCE.md](PERFORMANCE.md)** - Concurrent vs sequential modes

## 🎯 Trading Strategy

**Focus**: EUR/USD shorting opportunities

The system is designed to:
- ✅ Trade WITH major trends (never against the market)
- ✅ Find news-driven entry opportunities  
- ✅ Take small, lower-risk profits
- ✅ Calculate risk/reward on un-leveraged £100 positions
- ✅ Provide specific timing windows in UTC
- ❌ Avoid general market commentary without actionable timing

## 📊 How It Works

```
103 RSS Feeds → 6 Junior Analysts → Senior Manager → Executive Committee → Discord
```

1. **RSS Fetching** (Rate-limited, concurrent)
   - 103 feeds fetched with max 10 concurrent requests
   - Random delays to avoid blocking
   - ~30-60 seconds to fetch all sources

2. **Tier 1: Junior Analysts** (Concurrent or Sequential)
   - 6 analysts review news independently
   - Each has unique personality and temperature
   - Different AI models for diverse perspectives
   - ~2-5 minutes per analyst

3. **Tier 2: Senior Manager**
   - Synthesizes all 6 analyst reports
   - Identifies consensus and disagreements
   - Filters noise and conflicting signals
   - ~2-3 minutes

4. **Tier 3: Executive Committee**
   - Final decision-making layer
   - Verifies timing and risk/reward
   - Builds consensus on actionable trades
   - Formats output for Discord
   - ~2-3 minutes

**Total Time**: 10-20 minutes depending on mode and hardware

## ⚙️ Configuration

### Team Configuration (analyst_team.json)

The analyst team is fully configurable via JSON! Edit `analyst_team.json` to:
- ✅ Add/remove analysts
- ✅ Change AI models and temperatures
- ✅ Customize personalities and prompts
- ✅ Modify management layers

See **[ANALYST_CONFIG.md](ANALYST_CONFIG.md)** for full configuration guide.

### Environment Configuration (.env)

Key settings in `.env`:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Execution mode: false = sequential (safer), true = concurrent (faster)
RUN_CONCURRENT=false

# Discord Configuration (optional but recommended)
DISCORD_WEBHOOK_URL=your_webhook_url_here

# Workflow Configuration
RUN_ONCE=true
SCHEDULE_INTERVAL_HOURS=1

# Logging
LOG_LEVEL=INFO
```

**Configuration Notes**:
- **RUN_CONCURRENT**: Set to `false` if your Ollama instance can't handle concurrent requests. Sequential is safer but slower.
- **Analyst Team**: Configured in `analyst_team.json` - no need to edit code!

## 📝 Reviewing AI Decisions

All analyst reports are automatically saved to the `reports/` folder for your review:

- **Reports are cleared on each run** - Only the latest analysis is kept
- **Individual reports** - Every analyst's output saved separately
- **Final summary** - Complete overview including what was sent to Discord
- **Organized by tier** - Easy to navigate junior → senior → executive reports

### Quick Access

After a run, check:
1. **`reports/FINAL_SUMMARY_*.txt`** - Complete overview and executive decisions
2. **`reports/tier3_executive_committees/`** - Final trading decisions
3. **`reports/tier2_senior_managers/`** - Synthesis and reasoning
4. **`reports/tier1_junior_analysts/`** - Detailed analysis by each analyst

See **[REPORTS_QUICK_REFERENCE.md](REPORTS_QUICK_REFERENCE.md)** for detailed guidance on reviewing reports.

### Getting a Discord Webhook URL

1. Open your Discord server
2. Go to Server Settings → Integrations → Webhooks
3. Click "New Webhook"
4. Choose a channel and copy the webhook URL
5. Paste it into your `.env` file

## 🎮 Usage

### Run Once

To run the workflow once:

```bash
python src/main.py
```

Or explicitly set in `.env`:
```env
RUN_ONCE=true
```

### Scheduled Execution

To run on a schedule (e.g., every hour):

1. Set in `.env`:
   ```env
   RUN_ONCE=false
   SCHEDULE_INTERVAL_HOURS=1
   ```

2. Run:
   ```bash
   python src/main.py
   ```

The workflow will run immediately and then repeat every hour. Press `Ctrl+C` to stop.

## How It Works

1. **Fetch RSS Feeds**: Retrieves articles from 8 forex news sources:
   - FXStreet (news and analysis)
   - InvestingLive
   - DailyForex (4 feeds: news, technical, fundamental, articles)
   - Newsquawk

2. **AI Analysis**: Processes news through 4 AI agents:
   - 1x DeepSeek model
   - 3x GPT-OSS models
   - Each agent analyzes for EUR/USD shorting opportunities and volatility timing

3. **Synthesis**: Combines all agent outputs into a single, actionable summary with:
   - Risk/reward analysis
   - Clear explanations of acronyms
   - Specific trade recommendations based on £100 investment
   - Time-sensitive alerts

4. **Discord Notification**: Sends the final summary to your Discord channel

## Project Structure

```
day-trader/
├── src/
│   ├── __init__.py
│   ├── main.py              # Workflow orchestrator
│   ├── config.py            # Configuration management
│   ├── rss_fetcher.py       # RSS feed fetching
│   ├── ai_analyzer.py       # Ollama AI analysis
│   └── discord_sender.py    # Discord integration
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration Options

All configuration is done via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Ollama API endpoint | `http://localhost:11434` |
| `OLLAMA_MODEL_20B` | Primary model | `gpt-oss:20b` |
| `OLLAMA_MODEL_DEEPSEEK` | Secondary model | `deepseek-r1:8b` |
| `DISCORD_WEBHOOK_URL` | Discord webhook | None (prints to console) |
| `RUN_ONCE` | Run once vs scheduled | `true` |
| `SCHEDULE_INTERVAL_HOURS` | Hours between runs | `1` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

## Troubleshooting

### Ollama Connection Issues

If you see connection errors:
```bash
# Check if Ollama is running
ollama list

# Start Ollama (if needed)
ollama serve
```

### Model Not Found

If a model isn't available:
```bash
ollama pull gpt-oss:20b
ollama pull deepseek-r1:8b
```

### Discord Not Working

- Ensure your webhook URL is correct in `.env`
- Check the webhook hasn't been deleted in Discord
- If no webhook is configured, results will print to console

### Import Errors

If you see import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Differences from n8n Workflow

- ✅ Same RSS sources
- ✅ Same AI models and prompts
- ✅ Same Discord integration
- ✅ Hourly scheduling support
- ➕ Rich CLI with progress indicators
- ➕ Better error handling and logging
- ➕ More flexible configuration
- ➕ Easier to version control and modify

## Contributing

Feel free to submit issues or pull requests!

## License

[Your License Here]
