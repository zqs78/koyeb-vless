#!/usr/bin/env python3
from aiohttp import web
import sys
import time

# 立即刷新输出
sys.stdout.flush()
sys.stderr.flush()

async def health_check(request):
    """健康检查端点"""
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless"
    })

def print_node_info():
    """打印节点信息"""
    domain = "useful-florette-u9duiccetr-daf26dc7.koyeb.app"
    tcp_proxy_domain = "01.proxy.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    info = f"""
============================================================
🎯 VLESS节点配置信息 (TCP代理版本)
============================================================
📍 地址: {tcp_proxy_domain}
🔢 端口: 17893
🔑 UUID: {uuid}
🌐 协议: vless
📡 传输: websocket
🛣️  路径: /
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vless://{uuid}@{tcp_proxy_domain}:17893?type=ws&path=%2F&security=tls&sni={domain}#Koyeb-VLESS-TCP

============================================================
🎯 VLESS节点配置信息 (直连版本)
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
vless://{uuid}@{domain}:443?type=ws&path=%2F&security=tls#Koyeb-VLESS-Direct
============================================================
"""
    # 强制输出
    print(info, flush=True)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    # 立即打印节点信息
    print("🔄 开始启动服务...")
    print_node_info()
    
    # 启动健康检查服务
    port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {port}")
    print("✅ 服务启动完成！")
    
    web.run_app(app, host='0.0.0.0', port=port, print=None)
