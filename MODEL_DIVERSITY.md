# Model Diversity Strategy

## Overview

This application uses **multiple AI agents with different models and temperatures** to get a diverse range of perspectives on forex news. The goal is to avoid groupthink and get more robust trading recommendations by synthesizing multiple viewpoints.

## Why Model Diversity?

### The Problem with Single Models
- Single AI models can be biased towards certain patterns
- Same model with same temperature gives similar answers
- Lack of diverse perspectives leads to blind spots

### The Solution: Agent Diversity
- **Multiple Models**: Different LLMs have different training data and reasoning patterns
- **Temperature Variation**: Same model at different temperatures gives different outputs
  - Lower temp (0.7): More conservative, focused on high-probability interpretations
  - Higher temp (1.0): More creative, considers edge cases and alternative scenarios
- **Synthesis**: Final model combines all perspectives, highlighting agreements and disagreements

## Configuration

### Model List
Configure AI agents in `.env`:

```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75
```

**Key Points**:
- Lists must be the same length (one temperature per model)
- You can use the same model multiple times with different temperatures
- Models are paired with temperatures in order: `(deepseek:8b, 0.7)`, `(gpt-oss:20b, 0.8)`, etc.

### Example Configurations

#### Conservative Setup (3 agents)
```env
AI_MODELS=gpt-oss:20b,gpt-oss:20b,deepseek-r1:8b
AI_TEMPERATURES=0.6,0.7,0.65
```
Lower temperatures, fewer models = faster, more focused analysis.

#### Diverse Setup (6 agents - default)
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest
AI_TEMPERATURES=0.7,0.8,0.9,1.0,0.85,0.75
```
Mix of models and temperatures = slower, more comprehensive analysis.

#### Maximum Diversity (8+ agents)
```env
AI_MODELS=deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,llama3:70b,llama3:70b,mistral:latest,mistral:latest,qwen:14b
AI_TEMPERATURES=0.6,0.7,0.9,0.75,0.95,0.7,1.0,0.8
```
Many models with varied temperatures = slowest, maximum perspective diversity.

## Execution Modes

### Sequential Mode (Default)
```env
RUN_CONCURRENT=false
```

**Pros**:
- Works reliably with Ollama (doesn't overload the server)
- Guaranteed to complete even on limited hardware
- Easier to debug issues

**Cons**:
- Slower (agents run one after another)
- Time = (num_agents × avg_agent_time) + synthesis_time

**When to Use**:
- Running Ollama locally on consumer hardware
- Your Ollama instance shows errors under concurrent load
- You want guaranteed stability over speed

### Concurrent Mode
```env
RUN_CONCURRENT=true
```

**Pros**:
- Much faster (all agents run simultaneously)
- Time = (max_agent_time) + synthesis_time
- Better utilization of server resources

**Cons**:
- Requires robust Ollama setup (server-grade hardware or API)
- May fail if Ollama can't handle parallel requests
- Higher memory usage

**When to Use**:
- Running Ollama on powerful server
- Using remote Ollama API with concurrent request support
- Need faster analysis and have the infrastructure

## How It Works

### 1. Agent Analysis Phase
Each AI agent analyzes the same forex news data independently:

```
Agent 1 (DeepSeek @ temp=0.7)    → Conservative analysis
Agent 2 (GPT-OSS @ temp=0.8)     → Slightly more creative
Agent 3 (GPT-OSS @ temp=0.9)     → More speculative
Agent 4 (GPT-OSS @ temp=1.0)     → Most creative
Agent 5 (Llama3 @ temp=0.85)     → Different model perspective
Agent 6 (Mistral @ temp=0.75)    → Another model's view
```

Each agent receives the same prompt and data but produces different insights based on:
- Model architecture and training data
- Temperature setting (randomness/creativity)

### 2. Synthesis Phase
A final synthesis agent (typically `gpt-oss:20b` at temp=0.7) combines all analyses:

```
Synthesis Agent (GPT-OSS @ temp=0.7)
├─ Reviews all 6 agent analyses
├─ Identifies areas of agreement
├─ Notes significant disagreements
├─ Synthesizes into final recommendation
└─ Provides confidence level based on consensus
```

The synthesis prompt specifically asks the model to:
- Highlight where agents agree (strong signals)
- Note where agents disagree (uncertainty/risk)
- Provide balanced final recommendation

## Temperature Guide

| Temperature | Behavior | Use Case |
|------------|----------|----------|
| 0.5-0.7 | Very focused, repeatable | Conservative base analysis |
| 0.7-0.8 | Balanced, slight variation | Default analysis |
| 0.8-0.9 | Creative, considers alternatives | Exploring edge cases |
| 0.9-1.0 | Highly creative, diverse outputs | Maximum divergence |

## Best Practices

### 1. Start Conservative
Begin with 3-4 agents at moderate temperatures:
```env
AI_MODELS=gpt-oss:20b,gpt-oss:20b,deepseek-r1:8b
AI_TEMPERATURES=0.7,0.8,0.75
```

### 2. Add Diversity Gradually
Once stable, add more models or temperature variance:
```env
AI_MODELS=gpt-oss:20b,gpt-oss:20b,deepseek-r1:8b,llama3:70b
AI_TEMPERATURES=0.7,0.9,0.75,0.85
```

### 3. Test Sequential First
Always test with `RUN_CONCURRENT=false` before enabling concurrent mode.

### 4. Monitor Synthesis Quality
Watch for:
- ✅ Good: Synthesis notes where agents agree/disagree
- ✅ Good: Clear confidence levels based on consensus
- ❌ Bad: Synthesis just repeats one agent's view
- ❌ Bad: Contradictory recommendations in synthesis

### 5. Balance Speed vs. Diversity
- **Need fast results**: 3 agents, sequential mode
- **Need diverse perspectives**: 6+ agents, varied temps
- **Production use**: Start conservative, scale up as needed

## Troubleshooting

### "Ollama connection refused" during concurrent mode
**Solution**: Switch to sequential mode (`RUN_CONCURRENT=false`)

### All agents giving same answer
**Solution**: Increase temperature variance (0.7, 0.85, 1.0 instead of 0.7, 0.75, 0.8)

### Synthesis is bland/generic
**Solution**: Add more diverse models, not just temperature variations

### Process takes too long
**Solution**: Reduce number of agents or try concurrent mode (if hardware supports)

### Out of memory errors
**Solution**: Reduce number of agents or use smaller models (7b instead of 70b)

## Example Output

With diverse models and temperatures, you might see:

```
Agent 1 (DeepSeek @ 0.7): EUR/USD likely to consolidate based on technical levels
Agent 2 (GPT-OSS @ 0.8): EUR/USD consolidation probable, slight upside bias
Agent 3 (GPT-OSS @ 0.9): EUR/USD could break higher if NFP disappoints
Agent 4 (GPT-OSS @ 1.0): EUR/USD breakout scenario possible, watch 1.0850
Agent 5 (Llama3 @ 0.85): EUR/USD range-bound, unclear direction
Agent 6 (Mistral @ 0.75): EUR/USD consolidation near current levels

Synthesis: Consensus suggests EUR/USD consolidation with slight upside bias.
4 of 6 agents favor range-bound movement. 2 agents see breakout potential.
Recommendation: Neutral to slight long bias. Key level: 1.0850 resistance.
```

Notice how:
- Lower temp agents (0.7, 0.75) are more conservative
- Higher temp agents (0.9, 1.0) consider breakout scenarios
- Different models (Llama3, Mistral) add unique perspectives
- Synthesis acknowledges the 4-2 split in agent opinions

## Summary

Model diversity is about:
- 🎯 **Getting multiple perspectives** on the same data
- 🔀 **Using different models** (DeepSeek, GPT-OSS, Llama3, Mistral)
- 🌡️ **Varying temperatures** (0.7-1.0) for different creativity levels
- 🤝 **Synthesizing insights** to find consensus and disagreement
- ⚖️ **Balancing speed** (sequential) vs **robustness** (more agents)

This approach helps avoid single-model bias and produces more robust trading signals.
