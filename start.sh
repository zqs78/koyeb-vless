#!/bin/sh

echo "🚀 开始启动Xray服务..."

# 打印节点信息
echo "
============================================================
🎯 VLESS节点配置信息
============================================================
📍 地址: useful-florette-u9duiccetr-daf26dc7.koyeb.app
🔢 端口: 443
🔑 UUID: 258751a7-eb14-47dc-8d18-511c3472220f
🌐 协议: vless
📡 传输: websocket
🛣️  路径: /
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vless://258751a7-eb14-47dc-8d18-511c3472220f@useful-florette-u9duiccetr-daf26dc7.koyeb.app:443?type=ws&path=%2F&security=tls#Koyeb-VLESS
============================================================
"

# 启动Xray
exec /usr/local/bin/xray run -config /app/config.json
