#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const POEM_FILE = '/home/admin/.openclaw/workspace/tang-poetry/蒙学/tangshisanbaishou.json';
const STATE_FILE = '/home/admin/.openclaw/workspace/memory/poem-state.json';

// 读取诗歌文件
const poetry = JSON.parse(fs.readFileSync(POEM_FILE, 'utf-8'));
const allPoems = poetry.content.flatMap(section => section.content);

// 读取或初始化状态
let state = { index: 0 };
if (fs.existsSync(STATE_FILE)) {
  state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
}

// 获取下一首诗（循环）
const poemIndex = state.index % allPoems.length;
const poem = allPoems[poemIndex];

// 格式化诗歌内容
let message = `📖 **${poem.chapter}**\n`;
if (poem.subchapter) {
  message += `_${poem.subchapter}_\n\n`;
} else {
  message += `\n`;
}
message += `✍️ ${poem.author}\n\n`;
message += poem.paragraphs.join('\n');

// 发送消息（通过 openclaw message 命令）
try {
  execSync(`openclaw message send --target "telegram:8750402924" --message "${message.replace(/"/g, '\\"')}"`, {
    stdio: 'pipe'
  });
  console.log(`Sent poem ${poemIndex + 1}/${allPoems.length}: ${poem.chapter}`);
} catch (error) {
  console.error('Failed to send message:', error.message);
  process.exit(1);
}

// 更新状态
state.index = poemIndex + 1;
fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
