#!/bin/sh

echo "🚀 开始启动服务..."

# 检查端口权限
echo "🔍 检查端口权限..."
netstat -tuln | grep 443 || echo "端口443未监听（正常）"

# 启动Xray服务（非root用户需要特殊权限）
echo "📡 启动Xray服务..."
if [ $(id -u) -eq 0 ]; then
    # 如果是root用户，使用setcap赋予绑定低端口权限
    setcap 'cap_net_bind_service=+ep' /usr/local/bin/xray
    su xrayuser -c "/usr/local/bin/xray run -config /app/config.json &"
else
    # 如果不是root用户，直接启动
    /usr/local/bin/xray run -config /app/config.json &
fi

# 等待Xray启动
sleep 3

# 检查Xray是否启动
if pgrep xray > /dev/null; then
    echo "✅ Xray服务启动成功"
else
    echo "❌ Xray服务启动失败"
fi

# 启动健康检查服务
echo "🩺 启动健康检查服务..."
python3 /app/main.py
