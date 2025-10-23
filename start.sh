#!/bin/sh
echo "🚀 开始启动服务..."
echo "📡 启动Xray服务..."
/usr/local/bin/xray run -config /app/config.json &
echo "🩺 启动健康检查服务..."
python3 /app/main.py
