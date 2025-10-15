# Developer Guide

This guide explains how to modify and extend the Day Trader workflow.

## Project Structure

```
src/
├── __init__.py              # Package marker
├── main.py                  # Workflow orchestrator
├── config.py                # Configuration (environment variables)
├── rss_fetcher.py           # RSS feed fetching
├── ai_analyzer.py           # AI analysis with Ollama
└── discord_sender.py        # Discord webhook integration
```

## Common Modifications

### Adding a New RSS Feed

Edit `src/rss_fetcher.py`:

```python
class RSSFeedAggregator:
    def __init__(self):
        self.feeds = [
            # ... existing feeds ...
            RSSFeed("Your Feed Name", "https://example.com/rss"),
        ]
```

### Changing AI Models

Edit `.env`:

```env
OLLAMA_MODEL_20B=llama3:70b
OLLAMA_MODEL_DEEPSEEK=mistral:latest
```

Or modify `src/config.py` to change defaults.

### Adjusting Agent Count

Edit `src/ai_analyzer.py` in the `ForexAnalysisPipeline.analyze_news()` method:

```python
analyzers = [
    ("Agent 1", OllamaAnalyzer(self.ollama_base_url, self.model_deepseek)),
    ("Agent 2", OllamaAnalyzer(self.ollama_base_url, self.model_20b)),
    # Add or remove agents here
]
```

### Modifying AI Prompts

Edit the prompts in `src/ai_analyzer.py`:

```python
class ForexAnalysisPipeline:
    ANALYSIS_PROMPT = """Your custom prompt here..."""
    
    SYNTHESIS_PROMPT = """Your custom synthesis prompt..."""
```

### Changing Schedule Interval

Edit `.env`:

```env
SCHEDULE_INTERVAL_HOURS=2  # Run every 2 hours
```

### Adding More Output Channels

Create a new module (e.g., `src/slack_sender.py`) following the pattern in `discord_sender.py`, then integrate in `main.py`:

```python
from slack_sender import SlackSender

class SquawkWorkflow:
    def __init__(self):
        # ... existing ...
        self.slack_sender = SlackSender(settings.slack_webhook_url)
    
    def run(self):
        # ... existing steps ...
        self.slack_sender.send_message(analysis_result)
```

## Adding New Features

### Example: Article Caching

To avoid re-analyzing the same articles:

1. Create `src/cache.py`:

```python
import json
import hashlib
from pathlib import Path

class ArticleCache:
    def __init__(self, cache_file=".article_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache = self._load()
    
    def _load(self):
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text())
        return {}
    
    def _save(self):
        self.cache_file.write_text(json.dumps(self.cache))
    
    def is_seen(self, article):
        article_hash = hashlib.md5(
            article["link"].encode()
        ).hexdigest()
        return article_hash in self.cache
    
    def mark_seen(self, article):
        article_hash = hashlib.md5(
            article["link"].encode()
        ).hexdigest()
        self.cache[article_hash] = True
        self._save()
```

2. Use in `src/rss_fetcher.py`:

```python
from cache import ArticleCache

class RSSFeedAggregator:
    def __init__(self):
        self.feeds = [...]
        self.cache = ArticleCache()
    
    def fetch_all(self):
        all_entries = []
        for feed in self.feeds:
            entries = feed.fetch()
            # Filter out cached articles
            new_entries = [
                e for e in entries 
                if not self.cache.is_seen(e)
            ]
            for entry in new_entries:
                self.cache.mark_seen(entry)
            all_entries.extend(new_entries)
        return {"data": all_entries}
```

### Example: Logging to File

Modify `src/main.py`:

```python
import logging
from datetime import datetime

# Setup logging
log_file = f"logs/workflow_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SquawkWorkflow:
    def run(self):
        logger.info("Starting workflow")
        # ... rest of workflow ...
        logger.info("Workflow complete")
```

### Example: Multiple Trading Pairs

Modify the AI prompts to analyze multiple pairs:

```python
ANALYSIS_PROMPT = """You are reviewing forex news. Analyze for:
- EUR/USD shorting opportunities
- GBP/USD trading opportunities  
- USD/JPY trends

For each pair, note timing and risk/reward...
"""
```

## Testing

### Manual Testing

```powershell
# Test RSS fetching only
python -c "from src.rss_fetcher import RSSFeedAggregator; agg = RSSFeedAggregator(); print(len(agg.fetch_all()['data']), 'articles')"

# Test Ollama connection
python -c "import httpx; print(httpx.get('http://localhost:11434/api/tags').json())"

# Test Discord webhook
python -c "from src.discord_sender import DiscordSender; DiscordSender('YOUR_WEBHOOK').send_message('Test')"
```

### Unit Tests

Create `tests/test_rss_fetcher.py`:

```python
import pytest
from src.rss_fetcher import RSSFeed

def test_rss_feed_fetch():
    feed = RSSFeed("Test", "https://www.fxstreet.com/rss/news")
    entries = feed.fetch()
    assert len(entries) > 0
    assert "title" in entries[0]
```

Run with:
```powershell
pip install pytest
pytest tests/
```

## Debugging

### Enable Debug Logging

Edit `.env`:
```env
LOG_LEVEL=DEBUG
```

### Print Data at Each Step

Add debug prints in `src/main.py`:

```python
def run(self):
    # After RSS fetch
    console.print(f"[dim]Debug: Fetched {len(aggregated_data['data'])} articles[/dim]")
    
    # After analysis
    console.print(f"[dim]Debug: Analysis length: {len(analysis_result)} chars[/dim]")
```

### Use Rich Inspect

For detailed object inspection:

```python
from rich import inspect

# In any file
inspect(your_object, methods=True)
```

## Performance Optimization

### Parallel RSS Fetching

Use `asyncio` for faster fetching:

```python
import asyncio
import httpx

async def fetch_feed_async(feed):
    async with httpx.AsyncClient() as client:
        response = await client.get(feed.url)
        return feedparser.parse(response.text)

async def fetch_all_async(feeds):
    tasks = [fetch_feed_async(feed) for feed in feeds]
    return await asyncio.gather(*tasks)
```

### Smaller Models

Use smaller/faster models in `.env`:

```env
OLLAMA_MODEL_20B=llama3:8b  # Smaller, faster
OLLAMA_MODEL_DEEPSEEK=mistral:7b
```

### Reduce Agent Count

Edit `src/ai_analyzer.py` to use fewer agents:

```python
analyzers = [
    ("Agent 1", OllamaAnalyzer(self.ollama_base_url, self.model_20b)),
    # Only 1 agent instead of 4
]
```

## Common Issues

### "Module not found"

```powershell
pip install -r requirements.txt
```

### Ollama timeout

Increase timeout in `src/ai_analyzer.py`:

```python
self.client = httpx.Client(timeout=600.0)  # 10 minutes
```

### Memory issues

Reduce agent count or use smaller models.

### Discord character limit

Already handled - auto-truncates to 2000 chars.

## Best Practices

1. **Keep prompts in code** - Easier to version control
2. **Use environment variables** - For secrets and config
3. **Log important events** - Helps debugging
4. **Handle errors gracefully** - Don't crash on one bad feed
5. **Test incrementally** - Test each component separately
6. **Document changes** - Update README when adding features

## Contributing

When making changes:

1. Test locally first
2. Update documentation
3. Commit with clear messages
4. Consider backward compatibility

## Resources

- **Rich docs**: https://rich.readthedocs.io/
- **Pydantic docs**: https://docs.pydantic.dev/
- **Ollama docs**: https://github.com/ollama/ollama
- **Discord webhooks**: https://discord.com/developers/docs/resources/webhook

## Support

For issues or questions:
1. Check `verify_setup.py` output
2. Review logs
3. Check GitHub issues (if applicable)
4. Consult documentation files
