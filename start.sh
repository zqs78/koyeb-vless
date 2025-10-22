#!/bin/bash

# 启动 Xray VLESS 服务
echo "🚀 启动 Xray VLESS 服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &

# 等待 Xray 启动
sleep 5

# 启动健康检查服务
echo "🩺 启动健康检查服务..."
python3 health_check.py
