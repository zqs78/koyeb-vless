#!/bin/bash

# 启动 Xray 和健康检查服务
xray run -config /etc/xray/config.json &
python3 main.py
