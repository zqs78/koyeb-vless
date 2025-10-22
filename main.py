#!/usr/bin/env python3
import socket
import struct
import asyncio
from aiohttp import web
import os

# ！！！重要：请务必更改这个UUID，不要使用默认的！！！
UUID = "258751a7-eb14-47dc-8d18-511c3472220f"  # 请务必替换成你自己的UUID！

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

def print_node_info():
    """打印VLESS节点信息 - 修正版本"""
    # 尝试从环境变量获取域名，如果获取不到则提示用户手动填写
    koyeb_service_domain = os.environ.get('KOYEB_SERVICE_DOMAIN', '')
    if not koyeb_service_domain:
        # 尝试从其他环境变量获取
        koyeb_service_domain = os.environ.get('KOYEB_SERVICE_FQDN', '')
    
    print("\n" + "="*60)
    print("🎯 VLESS节点配置信息（请复制以下信息到客户端）")
    print("="*60)
    
    if koyeb_service_domain:
        print(f"📍 地址(address): {koyeb_service_domain}")
        print(f"🔢 端口(port): 33333")  # 修正为实际监听端口
        print(f"🔑 用户ID(UUID): {UUID}")
        print(f"🌐 传输协议(network): ws")
        print(f"🛣️  路径(path): /")
        print(f"🔒 传输安全(security): tls")
        print(f"📋 协议(protocol): vless")
        print("-"*60)
        
        # 生成VLESS链接
        vless_link = f"vless://{UUID}@{koyeb_service_domain}:33333?security=tls&type=ws&path=%2F#Koyeb-VLESS"
        print("🔗 VLESS链接：")
        print(vless_link)
    else:
        print("⚠️  无法自动获取域名，请手动填写：")
        print(f"📍 地址(address): [请在Koyeb控制台查找你的域名]")
        print(f"🔢 端口(port): 33333")  # 修正为实际监听端口
        print(f"🔑 用户ID(UUID): {UUID}")
        print(f"🌐 传输协议(network): ws")
        print(f"🛣️  路径(path): /")
        print(f"🔒 传输安全(security): tls")
        print("\n💡 使用方法：")
        print("1. 登录Koyeb控制台，找到你的服务域名")
        print("2. 将域名填入上面的地址字段")
        print("3. 使用上述参数配置客户端")
    
    print("="*60)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/{path:.*}', handle_vless)
    return app

if __name__ == "__main__":
    # 启动时打印节点信息
    print_node_info()
    
    app = create_app()
    print("🚀 VLESS服务器启动中...")
    print("📡 服务运行在: http://0.0.0.0:33333")
    web.run_app(app, host='0.0.0.0', port=33333)
