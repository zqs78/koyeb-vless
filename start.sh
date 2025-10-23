#!/bin/bash

# 打印启动信息
echo "🚀 启动 Xray 和健康检查服务..."

# 先启动 Xray 服务
echo "🔧 启动 Xray 服务..."
xray run -config /etc/xray/config.json &

# 等待 Xray 启动
sleep 3

# 启动 Python 健康检查服务
echo "🔧 启动健康检查服务..."
python3 main.py
