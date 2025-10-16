# AI Analyst Team Reference

## The Team

### 1. Marcus (Conservative) 🛡️
**Role**: Risk Management Specialist  
**Personality**: Conservative, risk-averse, focuses on downside protection  
**Model**: llama3.2:latest  
**Temperature**: 0.3 (Very conservative)  
**Focus**: Risk assessment and capital preservation  

**What Marcus brings**: Protection against bad trades, identifies when NOT to trade, flags potential losses

---

### 2. Sarah (Technical) 📊
**Role**: Technical Analysis Expert  
**Personality**: Data-driven, pattern-focused, relies on technical indicators  
**Model**: qwen2.5:latest  
**Temperature**: 0.5 (Balanced)  
**Focus**: Chart patterns, support/resistance levels, technical signals  

**What Sarah brings**: Technical entry/exit points, pattern recognition, price action analysis

---

### 3. James (Aggressive) 🚀
**Role**: Momentum Trader  
**Personality**: Aggressive, opportunity-seeking, high-conviction trades  
**Model**: mistral:latest  
**Temperature**: 0.8 (More creative)  
**Focus**: High-probability momentum plays and breakouts  

**What James brings**: Bold opportunities, identifies strong trending moves, finds conviction trades

---

### 4. Elena (Fundamental) 🌍
**Role**: Economic Policy Analyst  
**Personality**: Fundamental-focused, macro-economic perspective, central bank watcher  
**Model**: llama3.2:latest  
**Temperature**: 0.4 (Slightly conservative)  
**Focus**: Economic indicators, central bank policy, geopolitical events  

**What Elena brings**: Understanding WHY markets move, policy implications, economic data interpretation

---

### 5. David (Contrarian) 🔄
**Role**: Contrarian Strategist  
**Personality**: Skeptical, contrarian, questions consensus views  
**Model**: gemma2:latest  
**Temperature**: 0.7 (Creative)  
**Focus**: Identifying overcrowded trades and contrary indicators  

**What David brings**: Alternative perspectives, warnings about consensus traps, unique insights

---

### 6. Priya (Sentiment) 💭
**Role**: Market Sentiment Analyst  
**Personality**: Sentiment-focused, reads market mood, tracks positioning  
**Model**: phi3:latest  
**Temperature**: 0.6 (Moderately creative)  
**Focus**: Market sentiment, trader positioning, fear/greed indicators  

**What Priya brings**: Market psychology, sentiment shifts, crowd behavior analysis

---

## Temperature Scale Explained

- **0.3** (Marcus): Very focused, consistent, risk-averse responses
- **0.4** (Elena): Slightly conservative, analytical, structured thinking
- **0.5** (Sarah): Balanced, data-driven, neither too conservative nor creative
- **0.6** (Priya): Slightly creative, picks up on subtle market moods
- **0.7** (David): Creative, explores alternative viewpoints
- **0.8** (James): More creative, aggressive, finds bold opportunities

Higher temperature = More creative/diverse thinking  
Lower temperature = More focused/conservative thinking

---

## How They Work Together

### Common Agreement = Strong Signal
When **3+ analysts agree** on direction and timing, confidence is HIGH

### Split Opinions = Caution
When analysts disagree, the Senior Manager flags this and Executive Committee decides

### Complementary Strengths
- Marcus stops bad trades that others might miss
- James finds opportunities others might ignore
- Elena provides the "why" behind moves
- Sarah provides the "when" with technical timing
- David catches consensus traps
- Priya reads the room's emotional state

### Information Flow
1. All 6 analysts independently review the same news
2. Senior Manager synthesizes their reports
3. Executive Committee makes final decision
4. Output sent to Discord

---

## Customization

To modify analyst profiles, edit `ai_analyzer.py`:

```python
ANALYSTS = [
    AnalystProfile(
        name="Your Analyst Name",
        role="Their Job Title",
        personality="How they think/behave",
        model="ollama_model:tag",
        temperature=0.5,  # 0.0-1.0
        focus_area="What they focus on"
    ),
    # ... more analysts
]
```

**Recommended**: Keep 4-8 analysts for good coverage without excessive processing time
