FROM alpine:latest

# 安装必要的软件包
RUN apk update && apk add --no-cache \
    python3 \
    py3-aiohttp \
    curl \
    unzip \
    ca-certificates

# 安装xray-core
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm -rf xray.zip geoip.dat geosite.dat

# 创建工作目录
WORKDIR /app

# 复制文件
COPY config.json /etc/xray/config.json
COPY main.py .
COPY start.sh .

# 赋予启动脚本执行权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 8080 8000

# 使用启动脚本
CMD ["./start.sh"]
