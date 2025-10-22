#!/usr/bin/env python3
from aiohttp import web
import os

async def health_check(request):
    """健康检查端点"""
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless"
    })

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    # 健康检查运行在 8000 端口
    port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {port}")
    web.run_app(app, host='0.0.0.0', port=port)
