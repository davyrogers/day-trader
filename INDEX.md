# 📚 Day Trader - Documentation Index

Welcome! This is your complete guide to the Day Trader Forex News Analyzer.

## 🚀 Getting Started (Start Here!)

1. **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Quick overview and what was created
2. **[QUICKSTART.md](QUICKSTART.md)** - Fast track to running your first workflow
3. **[README.md](README.md)** - Complete user documentation

### Quick Commands

```powershell
# One-click installation
install.bat

# Verify setup
check_setup.bat

# Run workflow
start.bat
```

## 📖 Documentation Files

### User Documentation

| File | Purpose | When to Read |
|------|---------|--------------|
| **SETUP_SUMMARY.md** | Overview of what was created | First time setup |
| **QUICKSTART.md** | Fast start guide | Want to run ASAP |
| **CONFIG_REFERENCE.md** | Quick config examples | Need config help fast |
| **README.md** | Complete user manual | Full understanding |
| **MODEL_DIVERSITY.md** | AI agent diversity strategy | Configuring multiple models |
| **ARCHITECTURE.md** | System design & flow | Understanding internals |
| **PERFORMANCE.md** | Concurrent execution & speed | Performance details |
| **CONCURRENT_EXPLAINED.md** | How concurrent execution works | Sequential vs concurrent |
| **UPDATE_SUMMARY.md** | Latest changes and migration | Just updated the code |

### Developer Documentation

| File | Purpose | When to Read |
|------|---------|--------------|
| **DEVELOPER.md** | Modification & extension guide | Making changes |
| **ARCHITECTURE.md** | Technical architecture | Understanding code |

### Configuration Files

| File | Purpose |
|------|---------|
| **.env.example** | Environment template |
| **.env** | Your actual config (create from .env.example) |
| **requirements.txt** | Python dependencies |

## 🛠️ Helper Scripts

### Windows Batch Files

| Script | Purpose | Command |
|--------|---------|---------|
| **install.bat** | One-click setup | `install.bat` |
| **check_setup.bat** | Verify installation | `check_setup.bat` |
| **start.bat** | Run workflow | `start.bat` |

### Python Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| **run.py** | Main entry point | `python run.py` |
| **verify_setup.py** | Setup diagnostics | `python verify_setup.py` |

## 🗂️ Source Code

### Core Modules

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| **src/main.py** | Workflow orchestrator | `SquawkWorkflow`, `main()` |
| **src/config.py** | Configuration | `Settings` |
| **src/rss_fetcher.py** | RSS feed fetching | `RSSFeedAggregator`, `RSSFeed` |
| **src/ai_analyzer.py** | AI analysis | `ForexAnalysisPipeline`, `OllamaAnalyzer` |
| **src/discord_sender.py** | Discord integration | `DiscordSender` |

## 🎯 Common Tasks

### First Time Setup

1. Read: [SETUP_SUMMARY.md](SETUP_SUMMARY.md)
2. Run: `install.bat`
3. Edit: `.env` (add Discord webhook)
4. Run: `check_setup.bat`
5. Run: `start.bat`

### Daily Use

```powershell
# Run once
python run.py

# Or use the batch file
start.bat
```

### Making Changes

1. Read: [DEVELOPER.md](DEVELOPER.md)
2. Edit relevant source files
3. Test: `python run.py`
4. Update docs if needed

### Troubleshooting

1. Run: `python verify_setup.py`
2. Check: [README.md#troubleshooting](README.md#troubleshooting)
3. Review: Error messages in console

## 📊 Understanding the System

### High-Level Flow

```
RSS Feeds → Merge → AI Analysis (4 agents) → Synthesis → Discord
```

### Detailed Flow

See [ARCHITECTURE.md](ARCHITECTURE.md) for:
- System diagrams
- Data flow
- Component architecture
- Technology stack

### AI Pipeline

1. Fetch 200-400 articles from 8 RSS feeds
2. Analyze with 4 AI agents (3x GPT-OSS, 1x DeepSeek)
3. Synthesize into actionable trading advice
4. Send to Discord (or print to console)

## ⚙️ Configuration Options

All in `.env`:

```env
# Core Settings
OLLAMA_BASE_URL=http://localhost:11434
DISCORD_WEBHOOK_URL=your_webhook_here
RUN_ONCE=true
SCHEDULE_INTERVAL_HOURS=1

# Models
OLLAMA_MODEL_20B=gpt-oss:20b
OLLAMA_MODEL_DEEPSEEK=deepseek-r1:8b

# Logging
LOG_LEVEL=INFO
```

See [README.md#configuration](README.md) for details.

## 🔧 Customization Examples

### Add RSS Feed

Edit `src/rss_fetcher.py` - See [DEVELOPER.md#adding-a-new-rss-feed](DEVELOPER.md#adding-a-new-rss-feed)

### Change Models

Edit `.env` - See [DEVELOPER.md#changing-ai-models](DEVELOPER.md#changing-ai-models)

### Modify Prompts

Edit `src/ai_analyzer.py` - See [DEVELOPER.md#modifying-ai-prompts](DEVELOPER.md#modifying-ai-prompts)

### Add Output Channel

Create new sender module - See [DEVELOPER.md#adding-more-output-channels](DEVELOPER.md#adding-more-output-channels)

## 🐛 Troubleshooting Quick Reference

| Problem | Solution | Documentation |
|---------|----------|---------------|
| Import errors | `pip install -r requirements.txt` | [README.md](README.md#troubleshooting) |
| Ollama not found | `ollama serve` | [README.md](README.md#ollama-connection-issues) |
| Models missing | `ollama pull <model>` | [README.md](README.md#model-not-found) |
| Discord fails | Check webhook URL | [README.md](README.md#discord-not-working) |
| General issues | `python verify_setup.py` | [QUICKSTART.md](QUICKSTART.md#troubleshooting) |

## 📈 Performance

- **RSS Fetching**: 2-4 seconds (8 feeds in parallel)
- **AI Analysis**: 2-4 minutes (4 agents in parallel)
- **Discord Send**: < 1 second
- **Total**: **3-5 minutes per run** (3-4x faster with concurrency!)

See [PERFORMANCE.md](PERFORMANCE.md) for detailed benchmarks and optimization info.

## 🎓 Learning Path

### Beginner

1. [QUICKSTART.md](QUICKSTART.md) - Get it running
2. [README.md](README.md) - Understand features
3. Run a few times and review Discord output

### Intermediate

1. [ARCHITECTURE.md](ARCHITECTURE.md) - Understand system design
2. Review source code in `src/`
3. Try modifying prompts

### Advanced

1. [DEVELOPER.md](DEVELOPER.md) - Learn to extend
2. Add new features (caching, new sources, etc.)
3. Optimize performance

## 🆘 Getting Help

1. Check this index for relevant docs
2. Run `python verify_setup.py`
3. Review error messages carefully
4. Check [README.md#troubleshooting](README.md#troubleshooting)
5. Read [DEVELOPER.md](DEVELOPER.md) for code-level help

## ✅ Quick Checklist

### Before First Run

- [ ] Python 3.9+ installed
- [ ] Ollama installed and running
- [ ] Models downloaded (gpt-oss:20b, deepseek-r1:8b)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] Discord webhook URL added (optional)

### Ready to Run

- [ ] `python verify_setup.py` passes all checks
- [ ] You understand what the workflow does
- [ ] You know how to stop it (Ctrl+C)

### After Running

- [ ] Check Discord for analysis
- [ ] Review console output
- [ ] Verify no errors

## 🎉 Success Criteria

You're successful when:

✅ Workflow runs without errors  
✅ RSS feeds fetch successfully  
✅ AI analyses complete  
✅ Discord receives message (or console shows output)  
✅ You understand the trading recommendations  

## 📞 Quick Reference Card

```
┌────────────────────────────────────────┐
│     Day Trader Quick Reference         │
├────────────────────────────────────────┤
│ Setup:       install.bat               │
│ Verify:      check_setup.bat           │
│ Run Once:    start.bat                 │
│ Schedule:    Edit .env, run start.bat  │
│ Test:        python verify_setup.py    │
│ Docs:        INDEX.md (this file)      │
└────────────────────────────────────────┘
```

---

**Need something specific?** Use the table of contents above or search this file for keywords.

**Still can't find it?** Check [README.md](README.md) for comprehensive documentation.

**Want to modify?** See [DEVELOPER.md](DEVELOPER.md) for development guide.
