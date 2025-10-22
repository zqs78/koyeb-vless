#!/usr/bin/env python3
import asyncio
from aiohttp import web
import os

# ！！！重要：请务必更改这个UUID，不要使用默认的！！！
UUID = "258751a7-eb14-47dc-8d18-511c3472220f"

async def handle_vless(request):
    """简化版VLESS处理"""
    return web.Response(text="VLESS Proxy Server is Running")

async def health_check(request):
    """健康检查端点"""
    return web.json_response({"status": "ok", "service": "vless-proxy"})

def print_node_info():
    """打印节点信息"""
    domain = "religious-giacinta-mf5c9x1rio-c00bac2d.koyeb.app"
    
    print("\n" + "="*60)
    print("🎯 VLESS节点配置信息")
    print("="*60)
    print(f"📍 地址: {domain}")
    print(f"🔢 端口: 443")
    print(f"🔑 UUID: {UUID}")
    print(f"🌐 协议: vless")
    print(f"📡 传输: websocket")
    print(f"🛣️  路径: /")
    print(f"🔒 安全: tls")
    print("-"*60)
    
    vless_link = f"vless://{UUID}@{domain}:443?type=ws&security=tls&path=%2F#Koyeb-VLESS"
    print("🔗 分享链接:")
    print(vless_link)
    print("="*60)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/{path:.*}', handle_vless)
    return app

if __name__ == "__main__":
    print_node_info()
    
    port = int(os.environ.get('PORT', 33333))
    app = create_app()
    
    print(f"🚀 启动VLESS服务...")
    print(f"📡 监听端口: {port}")
    web.run_app(app, host='0.0.0.0', port=port)
