#!/usr/bin/env python3
from aiohttp import web
import asyncio
import threading
import time

async def handle_health(request):
    return web.Response(text='OK')

async def handle_status(request):
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless",
        "timestamp": time.time()
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

def run_web_app():
    app = web.Application()
    app.router.add_get('/', handle_health)
    app.router.add_get('/status', handle_status)
    
    web.run_app(app, host='0.0.0.0', port=8000, print=None)

if __name__ == "__main__":
    print("🔄 开始启动服务...")
    print_node_info()
    
    # 创建并启动web服务器线程
    web_thread = threading.Thread(target=run_web_app, daemon=True)
    web_thread.start()
    
    print("✅ 所有服务启动完成！")
    
    # 主线程保持运行
    try:
        while True:
            time.sleep(60)
            print("💓 服务运行中...")
    except KeyboardInterrupt:
        print("🛑 服务停止")
