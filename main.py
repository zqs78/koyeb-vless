#!/usr/bin/env python3
from aiohttp import web
import os
import sys

# 立即刷新输出缓冲区，确保信息显示在日志中
sys.stdout.flush()

async def health_check(request):
    """健康检查端点"""
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless"
    })

def print_node_info():
    """打印节点信息"""
    domain = "useful-florette-u9duiccetr-daf26dc7.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    tcp_port = "17893"
    
    info = f"""
============================================================
🎯 VLESS节点配置信息
============================================================
📍 地址: {domain}
🔢 端口: {tcp_port}
🔑 UUID: {uuid}
🌐 协议: vless
📡 传输: websocket
🛣️  路径: /
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vless://{uuid}@{domain}:{tcp_port}?type=ws&path=%2F&security=tls#Koyeb-VLESS
============================================================
"""
    print(info, flush=True)  # 强制刷新输出

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    # 立即打印节点信息
    print_node_info()
    
    # 启动健康检查服务
    port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {port}", flush=True)
    web.run_app(app, host='0.0.0.0', port=port, print=None)  # 禁用aiohttp的启动信息
