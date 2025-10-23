#!/usr/bin/env python3
from aiohttp import web
import sys
import subprocess
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
    tcp_proxy_domain = "01.proxy.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    info = f"""
============================================================
🎯 VLESS节点配置信息
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
vless://{uuid}@{tcp_proxy_domain}:17893?type=ws&path=%2F&security=tls#Koyeb-VLESS
============================================================
"""
    print(info, flush=True)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    # 立即打印节点信息
    print("🔄 开始启动服务...")
    print_node_info()
    
    # 启动Xray服务（在后台）
    print("🚀 启动Xray服务...")
    xray_process = subprocess.Popen([
        "/usr/local/bin/xray", 
        "run", 
        "-config", 
        "/etc/xray/config.json"
    ])
    
    # 等待Xray启动
    time.sleep(3)
    
    # 启动健康检查服务
    port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {port}")
    print("✅ 所有服务启动完成！")
    
    try:
        web.run_app(app, host='0.0.0.0', port=port, print=None)
    finally:
        # 确保Xray进程被终止
        xray_process.terminate()
        xray_process.wait()
