# 使用包含完整环境的基础镜像
FROM alpine:latest

# 安装必要的软件包
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    unzip \
    ca-certificates

# 安装xray-core（从官方release下载）
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm -rf xray.zip geoip.dat geosite.dat

# 创建工作目录
WORKDIR /app

# 复制配置文件
COPY config.json /etc/xray/config.json

# 复制健康检查脚本
COPY main.py .
COPY requirements.txt .

# 创建虚拟环境并安装Python依赖（修复pip安装问题）
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# 暴露端口
EXPOSE 33333 8000

# 启动命令（使用虚拟环境中的Python）
CMD sh -c 'xray run -config /etc/xray/config.json & /app/venv/bin/python3 main.py'
