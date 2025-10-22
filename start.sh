#!/bin/bash

# 启动 Xray 服务
echo "🚀 启动 Xray VLESS 服务..."
./xray run -config /etc/xray/config.json &

# 等待 Xray 启动
sleep 5

# 启动健康检查服务（在8000端口）
echo "🩺 启动健康检查服务（端口8000）..."
python3 main.py
