# Quick Configuration Reference

## TL;DR - Just Want It To Work?

Copy this into your `.env` file:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# AI Models (comma-separated, must match length of temperatures)
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75

# Synthesis (combines all agent results)
SYNTHESIS_MODEL=gpt-oss:20b
SYNTHESIS_TEMPERATURE=0.7

# Execution mode: false = one at a time (safer), true = all at once (faster)
RUN_CONCURRENT=false

# Discord
DISCORD_WEBHOOK_URL=your_webhook_here

# Workflow
RUN_ONCE=true
SCHEDULE_INTERVAL_HOURS=1

# Logging
LOG_LEVEL=INFO
```

Then install the models:
```powershell
ollama pull deepseek-r1:8b
ollama pull gpt-oss:20b
ollama pull llama3:70b
ollama pull mistral:latest
```

## Quick Configs

### Minimal (Fast & Simple)
Use if you only have 2 models installed:
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b
AI_TEMPERATURES=0.7,0.8,0.9
RUN_CONCURRENT=false
```
⏱️ Time: ~3-4 minutes

### Default (Balanced)
Good balance of diversity and speed:
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75
RUN_CONCURRENT=false
```
⏱️ Time: ~6-8 minutes

### Maximum Diversity
If you want all possible perspectives:
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,llama3:70b,mistral:latest,mistral:latest
AI_TEMPERATURES=0.6,0.7,0.85,1.0,0.75,0.95,0.8,0.9
RUN_CONCURRENT=false
```
⏱️ Time: ~10-15 minutes

### Speed Mode (Requires Powerful Ollama)
Same as default but concurrent:
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75
RUN_CONCURRENT=true  # ⚠️ Only if your Ollama can handle it
```
⏱️ Time: ~2-3 minutes (if Ollama supports concurrent requests)

## Configuration Rules

### ✅ DO:
- Keep `AI_MODELS` and `AI_TEMPERATURES` the same length
- Start with `RUN_CONCURRENT=false`
- Use temperature range 0.6-1.0
- Test with 3 agents before scaling to 6+

### ❌ DON'T:
- Mix up the order (models and temps are paired)
- Use `RUN_CONCURRENT=true` without testing first
- Use temperatures below 0.5 or above 1.0
- Start with 10+ agents (start small, scale up)

## Temperature Guide

| Value | Behavior | Good For |
|-------|----------|----------|
| 0.6-0.7 | Conservative, focused | Base analysis, key levels |
| 0.7-0.8 | Balanced | Default analysis |
| 0.8-0.9 | Creative | Alternative scenarios |
| 0.9-1.0 | Very creative | Edge cases, wild cards |

## Common Questions

### Q: How many agents should I use?
**A**: Start with 3, increase to 6 if you want more diversity. More than 8 is usually overkill.

### Q: Should I use concurrent mode?
**A**: Start with `false` (sequential). Only switch to `true` if:
- You have a powerful Ollama server
- Sequential mode is too slow for you
- You've tested and confirmed it works

### Q: Same model appears multiple times?
**A**: Yes! Using `gpt-oss:20b` three times with different temperatures (0.8, 0.9, 1.0) gives three different perspectives.

### Q: What if I only have 2 models?
**A**: Use them multiple times with different temperatures:
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b
AI_TEMPERATURES=0.7,0.8,0.9
```

### Q: Can I use different synthesis model?
**A**: Yes! Common choices:
```env
SYNTHESIS_MODEL=gpt-oss:20b    # Good for detailed synthesis
SYNTHESIS_MODEL=llama3:70b     # Good for balanced view
SYNTHESIS_MODEL=deepseek-r1:8b # Faster, still good
```

### Q: Why is synthesis temperature lower?
**A**: Synthesis should be focused and balanced (0.7), not creative. We want creativity in the agents, not the final summary.

## Troubleshooting

### "Lists must have the same length"
Make sure you have same number of models and temperatures:
```env
# ❌ Wrong - 3 models, 4 temps
AI_MODELS=model1,model2,model3
AI_TEMPERATURES=0.7,0.8,0.9,1.0

# ✅ Correct - 3 models, 3 temps
AI_MODELS=model1,model2,model3
AI_TEMPERATURES=0.7,0.8,0.9
```

### "Ollama connection refused" during concurrent
Switch to sequential:
```env
RUN_CONCURRENT=false
```

### Takes too long
Reduce number of agents:
```env
# Before (6 agents)
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75

# After (3 agents)
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b
AI_TEMPERATURES=0.7,0.8,0.9
```

### All agents give same answer
Increase temperature spread:
```env
# Before - too similar
AI_TEMPERATURES=0.7,0.75,0.8

# After - more diverse
AI_TEMPERATURES=0.7,0.85,1.0
```

## Migration from Old Config

If you have old `.env` with:
```env
OLLAMA_MODEL_20B=gpt-oss:20b
OLLAMA_MODEL_DEEPSEEK=deepseek-r1:8b
```

Just add the new variables (old ones are ignored):
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b
AI_TEMPERATURES=0.7,0.8,0.9
SYNTHESIS_MODEL=gpt-oss:20b
SYNTHESIS_TEMPERATURE=0.7
RUN_CONCURRENT=false
```

## Need More Help?

- **Quick Start**: Read `QUICKSTART.md`
- **Full Details**: Read `MODEL_DIVERSITY.md`
- **Architecture**: Read `ARCHITECTURE.md`
- **All Docs**: See `INDEX.md`
