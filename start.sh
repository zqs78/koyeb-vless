#!/bin/sh

echo "🚀 开始启动服务..."

# 先启动健康检查服务（监听8000端口）
echo "🩺 启动健康检查服务..."
python3 /app/health_check.py &

# 等待健康检查服务启动
sleep 2

# 再启动Xray服务（也监听8000端口，但通过不同路径区分）
echo "📡 启动Xray服务..."
/usr/local/bin/xray run -config /app/config.json
