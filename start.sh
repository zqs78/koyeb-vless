#!/bin/bash

# 验证 Xray 安装
echo "🔍 验证 Xray 安装..."
ls -la /usr/local/bin/xray
/usr/local/bin/xray version

# 启动 Xray VLESS 服务
echo "🚀 启动 Xray VLESS 服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &

# 等待 Xray 启动
sleep 5

# 检查 Xray 进程
echo "🔍 检查 Xray 进程..."
ps aux

# 启动健康检查服务
echo "🩺 启动健康检查服务..."
python3 main.py
