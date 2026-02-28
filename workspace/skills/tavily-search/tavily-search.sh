#!/bin/bash
# Tavily Search Script
# Usage: ./tavily-search.sh "query" [max_results]

QUERY="$1"
MAX_RESULTS="${2:-5}"
API_KEY="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"

if [ -z "$QUERY" ]; then
  echo "Usage: $0 \"query\" [max_results]"
  exit 1
fi

curl -s -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"$QUERY\",
    \"max_results\": $MAX_RESULTS,
    \"search_depth\": \"basic\",
    \"include_answer\": true
  }"
