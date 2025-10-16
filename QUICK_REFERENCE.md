# Quick Reference Card

## 🚀 Quick Start Commands

```bash
# Install everything
install.bat

# Run the analyzer
start.bat

# Or manually
python run.py
```

---

## 👥 The Team (Quick Reference)

| Analyst | Role | Temp | What They Do |
|---------|------|------|--------------|
| 🛡️ Marcus | Risk Mgmt | 0.3 | Stops bad trades, flags risks |
| 📊 Sarah | Technical | 0.5 | Chart patterns, timing |
| 🚀 James | Momentum | 0.8 | Bold opportunities |
| 🌍 Elena | Fundamental | 0.4 | Economic data, policy |
| 🔄 David | Contrarian | 0.7 | Alternative views |
| 💭 Priya | Sentiment | 0.6 | Market psychology |

---

## 📊 Pipeline at a Glance

```
┌───────────────────────────────────────────────┐
│  103 RSS FEEDS (30-60s)                       │
│  ↓                                            │
│  TIER 1: 6 Analysts Review (2-30min)          │
│  ↓                                            │
│  TIER 2: Senior Manager Synthesis (2-3min)    │
│  ↓                                            │
│  TIER 3: Executive Committee (2-3min)         │
│  ↓                                            │
│  DISCORD: Clear Trading Signal                │
└───────────────────────────────────────────────┘

Total: 10-40 minutes depending on mode
```

---

## ⚙️ Key Settings (.env)

```env
OLLAMA_BASE_URL=http://localhost:11434
DISCORD_WEBHOOK_URL=your_webhook_here
RUN_CONCURRENT=false    # true = faster, false = safer
RUN_ONCE=true          # false = scheduled
```

---

## 📦 Required Ollama Models

```bash
ollama pull llama3.2:latest
ollama pull qwen2.5:latest
ollama pull mistral:latest
ollama pull gemma2:latest
ollama pull phi3:latest
```

---

## 📝 Output Format (What You Get)

```
━━━━━━━━━━━━━━━━━━━━
🎯 TRADING SIGNAL
━━━━━━━━━━━━━━━━━━━━

📊 CONSENSUS: YES/NO/WATCH

⏰ KEY TIMES (UTC):
• HH:MM - Event description
• HH:MM - Event description

💹 TRADE SETUP:
Pair: EUR/USD
Direction: SHORT
Entry: X.XXXX
Stop: X.XXXX
Target: X.XXXX

Risk: £X on £100
Reward: £Y potential
Odds: XX% (reason)

⚠️ RISKS:
• Risk 1
• Risk 2

🎲 DECISION:
Clear recommendation here.
━━━━━━━━━━━━━━━━━━━━
```

---

## 🎯 Trading Rules

✅ **DO**:
- Trade WITH major trends
- Wait for specific time windows
- Use stop losses (mandatory)
- Follow consensus signals
- Check all 3 time windows

❌ **DON'T**:
- Trade against the trend
- Enter before data releases
- Ignore risk warnings
- Skip stop losses
- Trade on low consensus

---

## 📊 Consensus Levels

| Analysts Agree | Confidence | Action |
|----------------|------------|--------|
| 5-6 of 6 | Very High | Strong signal |
| 4 of 6 | High | Good signal |
| 3 of 6 | Medium | Conditional |
| 0-2 of 6 | Low | No trade |

---

## 🔧 Troubleshooting

**Problem**: "Connection refused to Ollama"  
**Solution**: Make sure Ollama is running (`ollama serve`)

**Problem**: "Model not found"  
**Solution**: Pull the model (`ollama pull model:tag`)

**Problem**: Analysis takes too long  
**Solution**: Use `RUN_CONCURRENT=false` for stability

**Problem**: Discord not receiving messages  
**Solution**: Check webhook URL in `.env` is correct

**Problem**: Out of memory  
**Solution**: Use sequential mode, close other apps

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `run.py` | Main entry point |
| `src/main.py` | Workflow orchestration |
| `src/rss_fetcher.py` | 103 RSS feeds |
| `src/ai_analyzer.py` | 3-tier AI pipeline |
| `src/discord_sender.py` | Discord integration |
| `.env` | Configuration |

---

## 📖 Full Documentation

- **[README.md](README.md)** - Overview & setup
- **[ANALYSIS_PIPELINE.md](ANALYSIS_PIPELINE.md)** - Architecture
- **[ANALYST_TEAM.md](ANALYST_TEAM.md)** - Meet the analysts
- **[SYSTEM_FLOW.md](SYSTEM_FLOW.md)** - Visual pipeline
- **[EXAMPLE_OUTPUTS.md](EXAMPLE_OUTPUTS.md)** - Sample outputs
- **[ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md)** - What's new

---

## 🎓 Understanding Temperature

| Temp | Behavior | Used By |
|------|----------|---------|
| 0.3 | Very conservative, focused | Marcus, Exec |
| 0.4 | Slightly conservative | Elena, Senior |
| 0.5 | Balanced | Sarah |
| 0.6 | Slightly creative | Priya |
| 0.7 | Creative, explorative | David |
| 0.8 | More creative, bold | James |

**Lower** = More predictable, risk-averse  
**Higher** = More creative, opportunity-seeking

---

## 💡 Tips for Best Results

1. **Run during market hours** (UTC 08:00-22:00) for best data
2. **Check before major news** (NFP, CPI, Fed meetings)
3. **Review all 3 time windows** provided in signal
4. **Always use stop losses** as specified
5. **Start with paper trading** to test signals
6. **Monitor Discord** for real-time updates
7. **Adjust for your timezone** (signals in UTC)

---

## 🚦 Signal Priority

| Signal Type | Action |
|-------------|--------|
| **CONSENSUS: YES** | High confidence - consider trade |
| **CONSENSUS: CONDITIONAL** | Wait for condition, then act |
| **CONSENSUS: WATCH** | Monitor but don't trade yet |
| **CONSENSUS: NO** | No trade opportunity today |

---

## ⏱️ Typical Timeline

```
00:00 - Start workflow
00:01 - Fetch 103 RSS feeds (30-60s)
00:02 - Junior analysts begin review
00:15 - Senior manager synthesis (varies)
00:18 - Executive committee decision
00:20 - Signal posted to Discord
```

**Sequential**: 20-40 minutes  
**Concurrent**: 10-20 minutes

---

## 🎯 Success Metrics

✅ **Good Signal**:
- Specific time windows
- Clear entry/exit levels
- Risk/reward calculated
- High consensus (4+)
- Conditions specified

❌ **Poor Signal**:
- Vague timing
- No specific levels
- Missing risk analysis
- Low consensus (0-2)
- Unclear action

---

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review error messages
3. Verify Ollama is running
4. Check Discord webhook
5. Try sequential mode

---

## 🔄 Update Workflow

```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt

# Re-pull Ollama models if needed
ollama pull llama3.2:latest
# ... etc
```

---

**Remember**: This system provides SIGNALS, not financial advice. Always do your own research and risk management!
