#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys
import asyncio
from aiohttp import web

# Xray进程
xray_process = None

def start_xray():
    """启动Xray服务"""
    global xray_process
    print("📡 启动Xray服务...")
    
    xray_process = subprocess.Popen([
        "/usr/local/bin/xray", 
        "run", 
        "-config", 
        "/app/config.json"
    ])
    
    # 等待Xray启动
    time.sleep(3)
    
    if xray_process.poll() is None:
        print("✅ Xray服务启动成功")
        return True
    else:
        print("❌ Xray服务启动失败")
        return False

def stop_xray():
    """停止Xray服务"""
    global xray_process
    if xray_process:
        print("🛑 停止Xray服务...")
        xray_process.terminate()
        xray_process.wait()

def signal_handler(sig, frame):
    """处理退出信号"""
    print("\n收到退出信号，正在停止服务...")
    stop_xray()
    sys.exit(0)

# 注册信号处理
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def health_check(request):
    """健康检查端点"""
    if xray_process and xray_process.poll() is None:
        return web.Response(text='OK')
    else:
        return web.Response(text='Xray服务异常', status=503)

async def main():
    """主函数"""
    print("🔄 开始启动服务...")
    
    # 打印节点信息
    domain = "useful-florette-u9duiccetr-daf26dc7.koyeb.app"
    uuid = "258751a7-eb14-47dc-8d18-511c3472220f"
    
    print(f"""
============================================================
🎯 VLESS节点配置信息
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
vless://{uuid}@{domain}:443?type=ws&path=%2F&security=tls#Koyeb-VLESS
============================================================
""")
    
    # 先启动Xray
    if not start_xray():
        print("❌ Xray启动失败，退出")
        return
    
    # 创建健康检查应用
    app = web.Application()
    app.router.add_get('/', health_check)
    
    # 启动健康检查服务（监听8000端口）
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    
    print("✅ 健康检查服务运行在端口: 8000")
    print("✅ 所有服务启动完成！")
    
    # 保持运行
    try:
        while True:
            await asyncio.sleep(10)
            if xray_process.poll() is not None:
                print("❌ Xray服务异常退出")
                break
    except KeyboardInterrupt:
        print("\n收到停止信号")
    finally:
        print("🛑 正在停止服务...")
        await runner.cleanup()
        stop_xray()

if __name__ == "__main__":
    asyncio.run(main())
