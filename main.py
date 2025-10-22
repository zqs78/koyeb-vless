#!/usr/bin/env python3
import socket
import struct
import asyncio
from aiohttp import web

# ！！！重要：请务必更改这个UUID，不要使用默认的！！！
# 你可以用这个命令在线生成一个：https://www.uuidgenerator.net/ 或者使用密码管理器生成
UUID = "a0b1c2d3-e4f5-6789-abcd-ef1234567890"  # 请务必替换成你自己的UUID！

async def handle_vless(request):
    reader = request.protocol._reader
    writer = request.protocol._writer
    try:
        # 读取并处理VLESS协议头
        data = await reader.read(1024)
        if len(data) < 24:
            return web.Response(status=400)
        
        # 验证UUID
        if data[:16] != bytes.fromhex(UUID.replace('-', '')):
            return web.Response(status=403)
        
        # 这里处理VLESS流量转发（核心逻辑）
        # 为简化示例，我们直接返回一个响应
        return web.Response(text="VLESS server is running on Koyeb")
    
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

async def health_check(request):
    """健康检查端点，Koyeb需要它"""
    return web.json_response({"status": "ok"})

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/{path:.*}', handle_vless)  # 捕获所有路径用于VLESS处理
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=33333)
