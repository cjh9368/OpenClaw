# Tavily Search Skill

Use Tavily AI-optimized search API for web searches.

## When to Use

- User asks for web search with Tavily
- Need AI-optimized search results with context
- Want cleaner, more relevant search results than traditional search engines

## Configuration

API Key is stored in the skill script.

## Usage

```bash
# Basic search
./tavily-search.sh "your query here"

# With max results
./tavily-search.sh "your query" 5
```

## API Key

`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`

## Response Format

Returns JSON with:
- `results`: Array of search results with `url`, `title`, `content`, `score`
- `query`: Original query
- `response_time`: Search time in seconds
