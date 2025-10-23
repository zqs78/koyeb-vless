#!/bin/sh

echo "🚀 开始启动服务..."

# 先启动Xray服务（监听8000端口）
echo "📡 启动Xray服务..."
/usr/local/bin/xray run -config /app/config.json &

# 等待Xray启动
sleep 3

# 检查Xray是否启动成功
if pgrep xray > /dev/null; then
    echo "✅ Xray服务启动成功"
else
    echo "❌ Xray服务启动失败"
    exit 1
fi

# 再启动健康检查服务（监听9000端口）
echo "🩺 启动健康检查服务..."
python3 /app/main.py
