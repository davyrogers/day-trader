# Per-Domain Rate Limiting

## What Changed

Updated from **global rate limiting** to **per-domain rate limiting** for RSS feed fetching.

## Why This Matters

### Before (Global Limit)
```
Max 10 concurrent requests TOTAL
└── All 103 feeds competing for 10 slots
    └── Even if hitting different domains
```

**Problem**: Different domains (fxstreet.com, reuters.com, etc.) don't care about each other's traffic. Global limit was too conservative.

### After (Per-Domain Limit)
```
Max 2 concurrent requests PER DOMAIN
├── fxstreet.com: 2 requests
├── investing.com: 2 requests  
├── reuters.com: 2 requests
├── marketwatch.com: 2 requests
└── ... (all domains can run in parallel)
```

**Benefit**: Much faster overall fetching while still being polite to individual servers.

## How It Works

### Domain Detection
```python
# Each feed extracts its domain
url = "https://www.fxstreet.com/rss/news"
domain = "www.fxstreet.com"  # Automatically extracted
```

### Per-Domain Semaphore
```python
# Each domain gets its own semaphore (limit: 2)
_domain_semaphores = {
    "www.fxstreet.com": Semaphore(2),
    "www.investing.com": Semaphore(2),
    "www.reuters.com": Semaphore(2),
    ...
}
```

### Concurrent Execution
```python
# Multiple domains fetch simultaneously
├── FXStreet feed 1  ]-- max 2 per domain
├── FXStreet feed 2  ]
├── Investing feed 1 ]-- max 2 per domain
├── Investing feed 2 ]
├── Reuters feed 1   ]-- max 2 per domain
└── ... (all at once!)
```

## Performance Impact

### Example with 103 feeds from ~40 domains

**Before (Global Limit: 10)**:
- 10 feeds fetch at a time
- ~10 batches needed
- ~30-60 seconds total

**After (Per-Domain Limit: 2)**:
- Up to 80+ feeds fetch simultaneously (2 per domain × 40 domains)
- 1-2 batches needed
- ~10-20 seconds total

**Result**: 2-3x faster! ⚡

## Configuration

Edit `src/rss_fetcher.py`:

```python
# Rate limiting configuration - PER DOMAIN
MAX_CONCURRENT_PER_DOMAIN = 2  # Adjust this (1-3 recommended)
REQUEST_DELAY_MIN = 0.1  # Delay before each request
REQUEST_DELAY_MAX = 0.3  # Maximum delay
```

### Recommended Settings

| Feeds | Domains | Concurrent/Domain | Expected Time |
|-------|---------|-------------------|---------------|
| 103 | 40 | 2 | 10-20 sec |
| 103 | 40 | 1 | 15-30 sec |
| 103 | 40 | 3 | 8-15 sec |

**Recommendation**: Keep at **2 concurrent per domain** - balances speed with server politeness.

## Benefits

1. ✅ **Faster Fetching**: Multiple domains in parallel
2. ✅ **Server Friendly**: Still rate-limited per domain
3. ✅ **No Blocking**: Respects individual server limits
4. ✅ **Automatic**: Domains detected automatically from URLs
5. ✅ **Scalable**: Add more feeds without slowing down

## Technical Details

### Global Semaphore Pool
```python
_domain_semaphores = defaultdict(
    lambda: asyncio.Semaphore(MAX_CONCURRENT_PER_DOMAIN)
)
```

- Each domain gets its own semaphore
- Created on-demand (first request to domain)
- Shared across all feeds from that domain
- Persists for the entire run

### Example Execution

```
Time 0s: Start all 103 feeds
         ├── fxstreet.com: 4 feeds → 2 start, 2 wait
         ├── investing.com: 7 feeds → 2 start, 5 wait
         ├── reuters.com: 2 feeds → 2 start
         └── ... (40+ domains all starting)

Time 2s: First completions
         ├── fxstreet.com: 2 complete → next 2 start
         ├── investing.com: 2 complete → next 2 start
         └── ...

Time 10-20s: All complete
```

## Error Handling

Errors are still per-feed:
```
✓ FXStreet - News: 25 articles
✗ Central Bank News: Failed - [Errno 11001] getaddrinfo failed
✓ FXStreet - Analysis: 18 articles
```

Failed feeds don't affect other domains.

## Monitoring

Watch the output:
```
Fetching 103 feeds from 42 domains (max 2 per domain)...
```

This tells you:
- **103 feeds**: Total feed count
- **42 domains**: Unique servers
- **max 2 per domain**: Rate limit per server

## Comparison

| Metric | Global Limit (10) | Per-Domain (2) |
|--------|------------------|----------------|
| Max simultaneous | 10 | 80+ |
| Politeness per server | ✅ Excellent | ✅ Excellent |
| Overall speed | ⚠️ Slow | ✅ Fast |
| Server load | ✅ Very low | ✅ Low |
| Blocking risk | ❌ Very unlikely | ❌ Very unlikely |

## Summary

**Old approach**: "Don't hit more than 10 servers at once"  
**New approach**: "Don't hit the same server more than 2 times at once"

**Result**: Much faster while remaining polite! 🚀

The system now intelligently manages requests per domain, allowing maximum parallelization while respecting server limits.
