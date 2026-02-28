#!/bin/bash
# 杭州天气日报 - Telegram 推送脚本
# 由 cron 每天 7:10 调用

# 设置环境变量
export PATH="/home/admin/.nvm/versions/node/v22.22.0/bin:$PATH"
export NODE_PATH="/home/admin/.nvm/versions/node/v22.22.0/lib/node_modules"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEATHER_SCRIPT="$SCRIPT_DIR/hangzhou-weather-daily.js"

# 获取天气报告
REPORT=$(node "$WEATHER_SCRIPT" 2>&1)

# 提取纯文本报告（去掉 JSON 部分）
REPORT_TEXT=$(echo "$REPORT" | sed '/^---JSON---$/,$d')

# 检查是否成功
if echo "$REPORT" | grep -q "❌ 获取天气失败"; then
    echo "天气获取失败"
    exit 1
fi

# 通过 OpenClaw 发送 Telegram 消息
# 使用用户的 chat ID (从 inbound context 获取)
CHAT_ID="8776343183"

/home/admin/.nvm/versions/node/v22.22.0/bin/openclaw message send \
    --channel telegram \
    --target "$CHAT_ID" \
    --message "$REPORT_TEXT" \
    --silent

if [ $? -eq 0 ]; then
    echo "✅ 天气报告已发送"
else
    echo "❌ 发送失败"
    exit 1
fi
