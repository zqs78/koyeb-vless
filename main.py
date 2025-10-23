#!/usr/bin/env python3
from aiohttp import web
import sys
import subprocess
import time

sys.stdout.flush()
sys.stderr.flush()

async def health_check(request):
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless"
    })

def print_node_info():
    # 使用Koyeb分配的动态端口
    tcp_proxy_domain = "01.proxy.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    info = f"""
============================================================
🎯 VLESS节点配置信息
============================================================
📍 地址: {tcp_proxy_domain}
🔢 端口: 请查看Koyeb控制台分配的TCP代理端口
🔑 UUID: {uuid}
🌐 协议: vless
📡 传输: websocket
🛣️  路径: /
🔒 安全: tls
------------------------------------------------------------
⚠️ 注意：TCP代理端口是动态分配的，请查看Koyeb控制台获取实际端口号
============================================================
"""
    print(info, flush=True)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    print("🔄 开始启动服务...")
    print_node_info()
    
    print("🚀 启动Xray服务...")
    xray_process = subprocess.Popen([
        "/usr/local/bin/xray", 
        "run", 
        "-config", 
        "/etc/xray/config.json"
    ])
    
    time.sleep(3)
    
    # 健康检查服务运行在8000端口
    port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {port}")
    print("✅ 所有服务启动完成！")
    
    try:
        web.run_app(app, host='0.0.0.0', port=port, print=None)
    finally:
        xray_process.terminate()
        xray_process.wait()
