#!/usr/bin/env python3
import socket
import struct
import asyncio
from aiohttp import web
import os

# ！！！重要：请务必更改这个UUID，不要使用默认的！！！
UUID = "258751a7-eb14-47dc-8d18-511c3472220f"  # 请务必替换成你自己的UUID！

async def handle_vless(request):
    """处理VLESS请求 - 修正版本"""
    try:
        # 检查是否是WebSocket请求
        if request.headers.get('Upgrade', '').lower() == 'websocket':
            # 处理WebSocket升级请求
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    await ws.send_str(f"Echo: {msg.data}")
                elif msg.type == web.WSMsgType.ERROR:
                    print(f'WebSocket错误: {ws.exception()}')
            
            return ws
        else:
            # 处理普通HTTP请求
            return web.Response(text="VLESS server is running on Koyeb")
    
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

async def health_check(request):
    """健康检查端点，Koyeb需要它"""
    return web.json_response({"status": "ok"})

def print_node_info():
    """打印VLESS节点信息 - 使用Koyeb环境变量"""
    # 使用Koyeb环境变量获取域名和端口
    koyeb_service_domain = os.environ.get('KOYEB_PUBLIC_DOMAIN', 'religious-giacinta-mf5c9x1rio-c00bac2d.koyeb.app')
    service_port = os.environ.get('PORT', '33333')
    
    print("\n" + "="*60)
    print("🎯 VLESS节点配置信息（请复制以下信息到客户端）")
    print("="*60)
    
    print(f"📍 地址(address): {koyeb_service_domain}")
    print(f"🔢 端口(port): 443")  # Koyeb外部访问使用443端口
    print(f"🔑 用户ID(UUID): {UUID}")
    print(f"🌐 传输协议(network): ws")
    print(f"🛣️  路径(path): /")
    print(f"🔒 传输安全(security): tls")
    print("-"*60)
    
    # 生成VLESS链接 - 外部使用443端口
    vless_link = f"vless://{UUID}@{koyeb_service_domain}:443?security=tls&type=ws&path=%2F#Koyeb-VLESS"
    print("🔗 VLESS链接：")
    print(vless_link)
    print("="*60)
    
    # 同时显示内部端口信息（用于调试）
    print(f"🔧 内部服务端口: {service_port}")
    print("="*60)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/{path:.*}', handle_vless)
    return app

if __name__ == "__main__":
    # 启动时打印节点信息
    print_node_info()
    
    # 使用Koyeb提供的PORT环境变量，如果没有则使用33333
    port = int(os.environ.get('PORT', 33333))
    
    app = create_app()
    print(f"🚀 VLESS服务器启动中...")
    print(f"📡 服务运行在: http://0.0.0.0:{port}")
    web.run_app(app, host='0.0.0.0', port=port)
