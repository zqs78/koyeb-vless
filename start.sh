#!/bin/sh

# 启动Xray服务
echo "🚀 启动Xray服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &

# 启动健康检查服务
echo "🩺 启动Python健康检查..."
python3 main.py
