# Forex News Squawk Analyzer

A Python-based workflow that replaces the n8n automation for analyzing forex news and generating trading signals.

## Features

- 🔄 Fetches RSS feeds from multiple forex news sources
- 🤖 AI-powered analysis using Ollama (multiple models)
- 💬 Sends summaries to Discord
- 📊 Rich CLI with progress indicators
- ⏰ Scheduled or one-time execution

## Setup

### Prerequisites

1. **Python 3.9+** installed
2. **Ollama** installed and running locally with the required models:
   - `gpt-oss:20b` (primary analysis model)
   - `deepseek-r1:8b` (secondary analysis model)
   - `llama3:70b` (optional, for more diverse perspectives)
   - `mistral:latest` (optional, for more diverse perspectives)

   Install models with:
   ```bash
   ollama pull gpt-oss:20b
   ollama pull deepseek-r1:8b
   ollama pull llama3:70b
   ollama pull mistral:latest
   ```

   **Note**: The system uses multiple AI agents with different temperatures (0.7-1.0) to get diverse perspectives on the forex news. You can configure which models to use and their temperatures in the `.env` file.

### Installation

1. Clone the repository (if not already done):
   ```bash
   git clone <your-repo-url>
   cd day-trader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   copy .env.example .env
   ```

4. Configure your `.env` file:
   ```env
   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   
   # AI Analysis Configuration
   # Comma-separated lists of models and temperatures (must match in length)
   AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
   AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75
   
   # Synthesis model (combines all agent analyses)
   SYNTHESIS_MODEL=gpt-oss:20b
   SYNTHESIS_TEMPERATURE=0.7
   
   # Execution mode: false = sequential (safer for Ollama), true = concurrent (faster)
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
   - **AI_MODELS**: List of Ollama models to use for analysis. Using the same model multiple times with different temperatures gives diverse perspectives.
   - **AI_TEMPERATURES**: Controls creativity/randomness (0.0-1.0). Higher = more creative. Must match length of AI_MODELS.
   - **RUN_CONCURRENT**: Set to `false` if your Ollama instance can't handle concurrent requests. Sequential is safer but slower.
   - **SYNTHESIS_MODEL**: The model used to combine all agent analyses into final recommendation.

### Getting a Discord Webhook URL

1. Open your Discord server
2. Go to Server Settings → Integrations → Webhooks
3. Click "New Webhook"
4. Choose a channel and copy the webhook URL
5. Paste it into your `.env` file

## Usage

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
