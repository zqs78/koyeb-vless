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
        "service": "xray-vmess"
    })

def print_node_info():
    """打印节点信息"""
    domain = "useful-florette-u9duiccetr-daf26dc7.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    info = f"""
============================================================
🎯 VMess节点配置信息
============================================================
📍 地址: {domain}
🔢 端口: 443
🔑 UUID: {uuid}
🌐 协议: vmess
📡 传输: websocket
🛣️  路径: /ray
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vmess://{uuid}@{domain}:443?type=ws&path=%2Fray&security=tls#Koyeb-VMess
============================================================
"""
    # 强制输出到标准错误（无缓冲）
    print(info, file=sys.stderr, flush=True)
    print(info, file=sys.stdout, flush=True)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    return app

if __name__ == "__main__":
    # 等待Xray启动
    time.sleep(2)
    
    # 打印节点信息
    print_node_info()
    
    # 启动健康检查服务
    port = 8000
    app = create_app()
    
    print(f"🩺 健康检查服务运行在端口: {port}", flush=True)
    web.run_app(app, host='0.0.0.0', port=port, print=None)
