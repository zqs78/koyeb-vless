#!/usr/bin/env python3
from aiohttp import web
import sys
import time
import subprocess
import socket

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
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    info = f"""
============================================================
🎯 VLESS节点配置信息
============================================================
📍 地址: {domain}
🔢 端口: 443
🔑 UUID: {uuid}
🌐 协议: vless
📡 传输: websocket
🛣️  路径: /vless
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vless://{uuid}@{domain}:443?type=ws&path=%2Fvless&security=tls#Koyeb-VLESS
============================================================
"""
    print(info, flush=True)

def is_port_available(port):
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except OSError:
            return False

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
    
    # 尝试不同的端口启动健康检查服务
    health_check_ports = [8080, 8081, 8082, 3000]
    app = None
    
    for port in health_check_ports:
        if is_port_available(port):
            app = create_app()
            print(f"🩺 健康检查服务运行在端口: {port}")
            print("✅ 所有服务启动完成！")
            
            try:
                web.run_app(app, host='0.0.0.0', port=port, print=None)
                break
            except OSError as e:
                print(f"❌ 端口 {port} 不可用: {e}")
                continue
    else:
        print("❌ 所有健康检查端口都不可用！")
        xray_process.terminate()
        xray_process.wait()
