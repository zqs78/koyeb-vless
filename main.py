#!/usr/bin/env python3
from aiohttp import web
import os

async def health_check(request):
    """健康检查端点"""
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless",
        "version": "1.8.4"
    })

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app = create_app()
    
    print(f"🩺 启动健康检查服务...")
    print(f"📡 监听端口: {port}")
    web.run_app(app, host='0.0.0.0', port=port)
