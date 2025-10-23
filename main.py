#!/usr/bin/env python3
import subprocess
import time
import signal
import sys
import http.server
import socketserver
import threading

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
        print("✅ Xray服务已停止")

def signal_handler(sig, frame):
    """处理退出信号"""
    print("\n收到退出信号，正在停止服务...")
    stop_xray()
    sys.exit(0)

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # 禁用日志输出
        pass

def start_health_check():
    """启动健康检查服务"""
    port = 8000
    try:
        with socketserver.TCPServer(("", port), HealthCheckHandler) as httpd:
            print(f"✅ 健康检查服务运行在端口: {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ 健康检查服务启动失败: {e}")

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
🛣️  路径: /
🔒 安全: tls
------------------------------------------------------------
🔗 分享链接:
vless://{uuid}@{domain}:443?type=ws&path=%2F&security=tls#Koyeb-VLESS
============================================================
"""
    print(info)

def main():
    """主函数"""
    print("🔄 开始启动服务...")
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print_node_info()
    
    # 启动健康检查服务（在后台线程）
    health_thread = threading.Thread(target=start_health_check)
    health_thread.daemon = True
    health_thread.start()
    
    # 启动Xray
    if not start_xray():
        print("❌ Xray启动失败")
        return
    
    print("✅ 所有服务启动完成！")
    
    # 保持运行
    try:
        while True:
            time.sleep(10)
            if xray_process and xray_process.poll() is not None:
                print("❌ Xray服务异常退出")
                break
    except KeyboardInterrupt:
        print("\n收到停止信号")
    finally:
        print("🛑 正在停止服务...")
        stop_xray()

if __name__ == "__main__":
    main()
