# Quick Start Guide

## 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 2. Install Ollama Models

Make sure Ollama is running, then:

```powershell
ollama pull gpt-oss:20b
ollama pull deepseek-r1:8b
```

## 3. Configure Environment

Copy the example environment file:

```powershell
copy .env.example .env
```

Edit `.env` and add your Discord webhook URL (optional):

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE
```

## 4. Run the Workflow

### Option A: Using the run script (recommended)

```powershell
python run.py
```

### Option B: Running directly

```powershell
python src\main.py
```

## 5. What You'll See

The workflow will:

1. ✅ Display a banner
2. 🔄 Fetch RSS feeds from 8 sources (with progress bar)
3. 🤖 Run 4 AI analyses (with progress bar)
4. 💬 Send results to Discord (or print to console if no webhook)
5. ✅ Display a summary

## Expected Output

```
╔═══════════════════════════════════════╗
║   FOREX NEWS SQUAWK ANALYZER          ║
╚═══════════════════════════════════════╝

Step 1: Fetching RSS Feeds
⠧ Fetching FXStreet - News...
✓ FXStreet - News: 50 articles
✓ FXStreet - Analysis: 30 articles
...

Total articles fetched: 300

Step 2: AI Analysis
⠙ Agent 1 (DeepSeek) analyzing...
✓ Agent 1 (DeepSeek) complete
✓ Agent 2 (GPT-OSS) complete
...

Step 3: Sending to Discord
✓ Message sent to Discord successfully

╔═══════════════════════════════════════╗
║              Summary                  ║
╠═══════════════════════════════════════╣
║ Workflow Complete!                    ║
║                                       ║
║ • Articles analyzed: 300              ║
║ • Time elapsed: 45.23 seconds         ║
║ • Completed at: 2025-10-15 14:30:00   ║
╚═══════════════════════════════════════╝
```

## Scheduled Execution

To run every hour automatically:

1. Edit `.env`:
   ```env
   RUN_ONCE=false
   SCHEDULE_INTERVAL_HOURS=1
   ```

2. Run:
   ```powershell
   python run.py
   ```

The workflow will run immediately and then repeat every hour. Press `Ctrl+C` to stop.

## Troubleshooting

### "Module not found" errors

```powershell
pip install -r requirements.txt
```

### Ollama connection errors

Check if Ollama is running:

```powershell
ollama list
```

If not running, start it:

```powershell
ollama serve
```

### Discord not working

- Check your webhook URL in `.env`
- Make sure the webhook exists in Discord
- If no webhook is set, the result will print to console (this is fine for testing)

## Next Steps

- ✅ Verify the workflow runs successfully
- ✅ Check Discord for the analysis message
- ✅ Adjust `SCHEDULE_INTERVAL_HOURS` if needed
- ✅ Review the analysis output
- ✅ Consider running as a scheduled task or service

## Tips

- The first run will take longer as models initialize
- Each run processes ~200-400 articles depending on news volume
- Analysis takes 2-5 minutes depending on your hardware
- Discord messages are limited to 2000 characters and will be truncated if longer
