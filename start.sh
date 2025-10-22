#!/bin/bash

# 验证 Xray 文件存在
echo "🔍 检查 Xray 二进制文件..."
ls -la /usr/local/bin/xray

# 启动 Xray VLESS 服务
echo "🚀 启动 Xray VLESS 服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &

# 等待 Xray 启动
sleep 5

# 检查 Xray 进程
echo "🔍 检查 Xray 进程..."
ps aux | grep xray

# 启动健康检查服务
echo "🩺 启动健康检查服务..."
python3 main.py
