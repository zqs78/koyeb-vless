#!/usr/bin/env python3
from aiohttp import web
import os
import time

async def health_check(request):
    return web.Response(text='OK')

async def status(request):
    return web.json_response({
        "status": "healthy",
        "service": "xray-vless",
        "timestamp": time.time(),
        "xray_running": os.system("pgrep xray > /dev/null") == 0
    })

def print_node_info():
    domain = "useful-florette-u9duiccetr-daf26dc7.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    info = f"""
============================================================
🎯 VLESS节点配置信息
============================================================
📍 地址: {domain}
🔢 端口: 443
🔑 UUID: {uuid}
🌐 协议: vless
📡 传输: websocket
🛣️  路径: /
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vless://{uuid}@{domain}:443?type=ws&path=%2F&security=tls#Koyeb-VLESS
============================================================
"""
    print(info)

app = web.Application()
app.router.add_get('/', health_check)
app.router.add_get('/status', status)

if __name__ == "__main__":
    print("🔄 开始启动服务...")
    print_node_info()
    print("✅ 健康检查服务运行在端口: 8000")
    web.run_app(app, host='0.0.0.0', port=8000, print=None)
