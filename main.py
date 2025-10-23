#!/usr/bin/env python3
from aiohttp import web
import sys
import socket
import subprocess
import time

sys.stdout.flush()
sys.stderr.flush()

async def health_check(request):
    return web.json_response({
        "status": "ok", 
        "service": "xray-vless"
    })

def is_port_open(port):
    """检查端口是否开放"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except OSError:
            return False

def print_node_info():
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
🔒 安全: none
------------------------------------------------------------
🔗 分享链接:
vless://{uuid}@{tcp_proxy_domain}:17893?type=ws&path=%2F#Koyeb-VLESS
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
    
    # 检查17893端口是否开放
    port_to_check = 17893
    if is_port_open(port_to_check):
        print(f"✅ 端口 {port_to_check} 可用")
    else:
        print(f"❌ 端口 {port_to_check} 不可用")
    
    # 启动Xray服务
    print("🚀 启动Xray服务...")
    xray_process = subprocess.Popen([
        "/usr/local/bin/xray", 
        "run", 
        "-config", 
        "/etc/xray/config.json"
    ])
    
    # 等待Xray启动
    time.sleep(5)
    
    # 再次检查端口
    if is_port_open(port_to_check):
        print(f"✅ Xray成功监听端口 {port_to_check}")
    else:
        print(f"❌ Xray未能监听端口 {port_to_check}")
    
    # 启动健康检查服务
    health_check_port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {health_check_port}")
    print("✅ 所有服务启动完成！")
    
    try:
        web.run_app(app, host='0.0.0.0', port=health_check_port, print=None)
    finally:
        # 确保Xray进程被终止
        xray_process.terminate()
        xray_process.wait()
