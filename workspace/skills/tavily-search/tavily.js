#!/usr/bin/env node
/**
 * Tavily Search Tool for OpenClaw
 * Usage: node tavily.js "search query" [max_results]
 */

const https = require('https');

const API_KEY = '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';
const query = process.argv[2];
const maxResults = parseInt(process.argv[3]) || 5;

if (!query) {
  console.error('Usage: node tavily.js "search query" [max_results]');
  process.exit(1);
}

const postData = JSON.stringify({
  query: query,
  max_results: maxResults,
  search_depth: 'basic',
  include_answer: true,
  include_domains: [],
  exclude_domains: []
});

const options = {
  hostname: 'api.tavily.com',
  port: 443,
  path: '/search',
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = https.request(options, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const result = JSON.parse(data);
      
      // Format output for human readability
      console.log(`\n🔍 Search Query: ${result.query}\n`);
      
      if (result.answer) {
        console.log(`💡 Answer: ${result.answer}\n`);
      }
      
      console.log(`📊 Results (${result.results.length} found):\n`);
      
      result.results.forEach((r, i) => {
        console.log(`${i + 1}. ${r.title}`);
        console.log(`   URL: ${r.url}`);
        console.log(`   Score: ${r.score}`);
        console.log(`   ${r.content.substring(0, 200)}${r.content.length > 200 ? '...' : ''}\n`);
      });
      
      console.log(`⏱️  Response time: ${result.response_time}s\n`);
      
      // Also output JSON for programmatic use
      console.log('---JSON---');
      console.log(JSON.stringify(result, null, 2));
      
    } catch (e) {
      console.error('Error parsing response:', e.message);
      console.error('Raw response:', data);
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('Request error:', e.message);
  process.exit(1);
});

req.write(postData);
req.end();
