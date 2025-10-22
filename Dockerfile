FROM ghcr.io/xtls/xray-core:latest

# 安装Python3用于健康检查
RUN apk add --no-cache python3 py3-pip

# 创建工作目录
WORKDIR /app

# 复制配置文件
COPY config.json /etc/xray/config.json

# 复制健康检查脚本
COPY main.py .
COPY requirements.txt .

# 安装Python依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 33333

# 启动命令（同时运行Xray和健康检查）
CMD sh -c 'xray run -config /etc/xray/config.json & python3 main.py'
