#!/usr/bin/env python3
from aiohttp import web
import os

async def health_check(request):
    return web.json_response({"status": "ok", "service": "xray-vless"})

def print_node_info():
    domain = "useful-florette-u9duiccetr-daf26dc7.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    print("\n" + "="*60)
    print("VLESS节点配置信息")
    print("="*60)
    print(f"地址: {domain}")
    print(f"端口: 443")
    print(f"UUID: {uuid}")
    print(f"协议: vless")
    print(f"传输: websocket")
    print(f"路径: /")
    print(f"安全: xtls")
    print("-"*60)
    
    vless_link = f"vless://{uuid}@{domain}:443?type=ws&security=xtls&path=%2F#Koyeb-VLESS"
    print("分享链接:")
    print(vless_link)
    print("="*60)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    print_node_info()
    port = 8000
    app = create_app()
    print(f"健康检查服务运行在端口: {port}")
    web.run_app(app, host='0.0.0.0', port=port)
