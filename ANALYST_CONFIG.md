# Analyst Team Configuration Guide

The `analyst_team.json` file allows you to fully configure your AI analyst team and management layers without touching the code.

## 📁 File Location

**Path**: `c:\Repos\day-trader\analyst_team.json`

This file is loaded automatically by the system on startup.

## 📋 Structure

```json
{
  "junior_analysts": [ ... ],
  "management_layers": [ ... ],
  "config_info": { ... }
}
```

## 👥 Junior Analysts Configuration

Each analyst needs these fields:

```json
{
  "name": "Marcus (Conservative)",
  "role": "Risk Management Specialist",
  "personality": "Conservative, risk-averse, focuses on downside protection",
  "model": "gpt-oss:20b",
  "temperature": 0.3,
  "focus_area": "Risk assessment and capital preservation",
  "system_prompt": "You are Marcus, a Risk Management Specialist..."
}
```

### Fields Explained

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Analyst's display name | "Marcus (Conservative)" |
| `role` | string | Their job title | "Risk Management Specialist" |
| `personality` | string | How they think/behave | "Conservative, risk-averse" |
| `model` | string | Ollama model to use | "gpt-oss:20b" |
| `temperature` | number | Creativity level (0.0-1.0) | 0.3 |
| `focus_area` | string | What they specialize in | "Risk assessment" |
| `system_prompt` | string | Full prompt instructions | See below |

### Temperature Guide

| Range | Behavior | Best For |
|-------|----------|----------|
| 0.0-0.3 | Very conservative, focused | Risk managers, executives |
| 0.4-0.6 | Balanced, analytical | Technical, fundamental analysts |
| 0.7-0.9 | Creative, explorative | Contrarian, aggressive traders |
| 1.0+ | Very creative (risky) | Not recommended |

### Available Models (Your Setup)

Based on your Ollama models:

| Model | Size | Speed | Best Use Case |
|-------|------|-------|---------------|
| `gpt-oss:20b` | 13GB | Fast | **Most capable** - senior roles, important decisions |
| `gpt-oss:120b` | 65GB | Slow | Very capable but CPU offload - use sparingly |
| `qwen3-coder:30b` | 18GB | Medium | Technical analysis, data-focused roles |
| `deepseek-r1:8b` | 5.2GB | Very Fast | Quick analyses, aggressive traders |
| `llama3.1:8b` | 4.9GB | Very Fast | Sentiment, quick perspectives |
| `gemma3:12b` | 8.1GB | Fast | Good all-rounder |
| `gemma3:4b` | 3.3GB | Very Fast | Lightweight analyses |

### System Prompt Tips

Your system prompt should:
1. ✅ Introduce the analyst's identity and role
2. ✅ Describe their personality and focus
3. ✅ Explain what they're analyzing (EUR/USD, news)
4. ✅ List critical requirements (timing, trends, risks)
5. ✅ Specify output format (times, confidence, etc.)
6. ✅ Remind them of the audience (senior management)

**Placeholder**: Use `{{ JSON.stringify($json.data, null, 2) }}` where news data should be injected (handled automatically by the system).

## 🏢 Management Layers Configuration

Each management layer needs these fields:

```json
{
  "name": "Senior Manager",
  "role": "Trading Desk Manager",
  "model": "gpt-oss:20b",
  "temperature": 0.4,
  "system_prompt": "You are the SENIOR TRADING MANAGER..."
}
```

### Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Layer name (must contain "senior" or "executive") |
| `role` | string | Management role description |
| `model` | string | Ollama model to use |
| `temperature` | number | Creativity level (keep low for management) |
| `system_prompt` | string | Full prompt instructions |

### Management Layer Types

The system automatically identifies:
- **Senior Manager**: Name contains "senior" or "manager" (Tier 2)
- **Executive Committee**: Name contains "executive" or "committee" (Tier 3)

**Recommendation**: Use `gpt-oss:20b` with low temperature (0.3-0.4) for management layers.

## ➕ Adding a New Analyst

1. Open `analyst_team.json`
2. Add to the `junior_analysts` array:

```json
{
  "name": "New Analyst Name",
  "role": "Their Job Title",
  "personality": "How they think",
  "model": "gpt-oss:20b",
  "temperature": 0.5,
  "focus_area": "What they focus on",
  "system_prompt": "You are [Name], a [Role]...\n\n[Full instructions]"
}
```

3. Save the file
4. Run the system - it will automatically load the new analyst!

## 🔧 Example Configurations

### Adding a Volatility Specialist

```json
{
  "name": "Rachel (Volatility)",
  "role": "Volatility Analyst",
  "personality": "Statistical, focuses on market swings and option pricing",
  "model": "qwen3-coder:30b",
  "temperature": 0.5,
  "focus_area": "Volatility forecasting and implied vol analysis",
  "system_prompt": "You are Rachel, a Volatility Analyst on a professional forex trading desk.\n\nPERSONALITY: Statistical, focuses on market swings and option pricing\nYOUR FOCUS: Volatility forecasting and implied vol analysis\n\n[Rest of standard prompt...]"
}
```

### Adding a News Flow Specialist

```json
{
  "name": "Tom (News Flow)",
  "role": "Real-Time News Analyst",
  "personality": "Fast-paced, focuses on breaking news impact",
  "model": "deepseek-r1:8b",
  "temperature": 0.7,
  "focus_area": "Real-time news interpretation and immediate market impact",
  "system_prompt": "You are Tom, a Real-Time News Analyst...\n\n[Instructions]"
}
```

### Using the 120B Model for Executive Committee

```json
{
  "name": "Executive Committee",
  "role": "Executive Decision Makers",
  "model": "gpt-oss:120b",
  "temperature": 0.2,
  "system_prompt": "You are the EXECUTIVE TRADING COMMITTEE...\n\n[Instructions]"
}
```

**Note**: `gpt-oss:120b` is slow but very capable. Use only for final executive decision if you have time.

## 📊 Optimal Configurations

### Speed-Focused (10-15 min total)

```json
"junior_analysts": [
  { "model": "deepseek-r1:8b", "temperature": 0.3, ... },
  { "model": "llama3.1:8b", "temperature": 0.5, ... },
  { "model": "gemma3:12b", "temperature": 0.7, ... },
  { "model": "deepseek-r1:8b", "temperature": 0.4, ... }
],
"management_layers": [
  { "model": "gpt-oss:20b", "temperature": 0.4, ... },
  { "model": "gpt-oss:20b", "temperature": 0.3, ... }
]
```

### Quality-Focused (20-30 min total)

```json
"junior_analysts": [
  { "model": "gpt-oss:20b", "temperature": 0.3, ... },
  { "model": "qwen3-coder:30b", "temperature": 0.5, ... },
  { "model": "gpt-oss:20b", "temperature": 0.8, ... },
  { "model": "gpt-oss:20b", "temperature": 0.4, ... },
  { "model": "gemma3:12b", "temperature": 0.7, ... },
  { "model": "llama3.1:8b", "temperature": 0.6, ... }
],
"management_layers": [
  { "model": "gpt-oss:20b", "temperature": 0.4, ... },
  { "model": "gpt-oss:20b", "temperature": 0.3, ... }
]
```

### Maximum Quality (30-60 min total)

Use `gpt-oss:20b` for all analysts with varied temperatures, plus `gpt-oss:120b` for executive committee.

## ⚠️ Common Mistakes

### ❌ Wrong Model Name
```json
"model": "gpt-oss-20b"  // Wrong (dash instead of colon)
```
✅ Correct:
```json
"model": "gpt-oss:20b"
```

### ❌ Temperature Out of Range
```json
"temperature": 1.5  // Too high (>1.0)
```
✅ Correct:
```json
"temperature": 0.8  // 0.0-1.0 range
```

### ❌ Missing Required Fields
```json
{
  "name": "Analyst",
  "model": "gpt-oss:20b"
  // Missing role, personality, temperature, etc.
}
```

### ❌ Invalid JSON
```json
{
  "name": "Analyst",  // Extra comma on last line
}
```

## 🧪 Testing Your Configuration

After editing, verify it loads:

```powershell
python -c "import json; json.load(open('analyst_team.json'))"
```

No output = Valid JSON ✅  
Error = Fix syntax ❌

## 🔄 Reloading Configuration

The configuration is loaded on startup. To apply changes:

1. Edit `analyst_team.json`
2. Save the file
3. Restart the application: `start.bat`

No need to edit Python code!

## 📖 Full Example

See the current `analyst_team.json` for a complete, working example with:
- 6 junior analysts with diverse personalities
- 2 management layers (senior manager + executive committee)
- Optimized model selection using your available models
- Complete system prompts

## 💡 Best Practices

1. **Start with 4-6 analysts** for good coverage without excessive time
2. **Use gpt-oss:20b** for critical roles (risk manager, executive committee)
3. **Vary temperatures** (0.3-0.8) for diverse perspectives
4. **Keep management temps low** (0.3-0.4) for conservative decisions
5. **Test incrementally** - add one analyst at a time
6. **Document changes** in config_info notes section

## 🎯 Recommended Team Compositions

### Minimal (4 analysts, ~10 min)
- Risk Manager (gpt-oss:20b, 0.3)
- Technical Analyst (qwen3-coder:30b, 0.5)
- Fundamental Analyst (gpt-oss:20b, 0.4)
- Sentiment Analyst (llama3.1:8b, 0.6)

### Balanced (6 analysts, ~15 min) ⭐ **Default**
Current configuration in file

### Comprehensive (8+ analysts, ~25 min)
Add to default:
- Volatility Specialist
- News Flow Analyst
- Correlation Trader
- Options Analyst

---

**Remember**: More analysts = better coverage but longer runtime. Find your balance!
