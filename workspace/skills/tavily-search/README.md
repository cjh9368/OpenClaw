# Tavily Search Skill for OpenClaw

AI-optimized web search using Tavily API.

## Quick Start

```bash
# Basic search
node /home/admin/.openclaw/workspace/skills/tavily-search/tavily.js "your query"

# With custom result count
node /home/admin/.openclaw/workspace/skills/tavily-search/tavily.js "your query" 10
```

## Features

- ✅ AI-generated answers with search results
- ✅ Relevance scoring for each result
- ✅ Clean, contextual content extraction
- ✅ Fast response times (~1-2 seconds)
- ✅ No API key setup needed (pre-configured)

## API Reference

**Endpoint:** `POST https://api.tavily.com/search`

**Headers:**
- `Authorization: Bearer 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`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "query": "search query",
  "max_results": 5,
  "search_depth": "basic",
  "include_answer": true,
  "include_domains": [],
  "exclude_domains": []
}
```

**Response:**
```json
{
  "query": "original query",
  "answer": "AI-generated answer",
  "results": [
    {
      "url": "https://...",
      "title": "Page Title",
      "content": "Extracted content",
      "score": 0.95
    }
  ],
  "response_time": 1.5
}
```

## Advanced Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_depth` | string | `"basic"` | `"basic"` or `"advanced"` |
| `max_results` | number | `5` | Max results (1-10) |
| `include_answer` | boolean | `false` | Include AI-generated answer |
| `include_raw_content` | boolean | `false` | Include raw page content |
| `include_domains` | array | `[]` | Only search these domains |
| `exclude_domains` | array | `[]` | Exclude these domains |
| `time_range` | string | `null` | `"day"`, `"week"`, `"month"`, `"year"` |
| `country` | string | `null` | Country code (e.g., `"us"`) |

## Examples

### Search with advanced depth
```bash
curl -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AI agents",
    "search_depth": "advanced",
    "max_results": 10
  }'
```

### Search specific time range
```bash
curl -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenClaw updates",
    "time_range": "week"
  }'
```

### Search only specific domains
```bash
curl -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenClaw documentation",
    "include_domains": ["docs.openclaw.ai", "github.com"]
  }'
```

## Other Tavily APIs

### Extract
Extract content from specific URLs:
```bash
curl -X POST https://api.tavily.com/extract \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "extract_depth": "basic"
  }'
```

### Research
Deep research with structured output:
```bash
curl -X POST https://api.tavily.com/research \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Research topic",
    "model": "auto"
  }'
```

## Resources

- [Tavily Documentation](https://docs.tavily.com/)
- [Tavily Playground](https://app.tavily.com/playground)
- [API Credits & Limits](https://docs.tavily.com/documentation/api-credits)
