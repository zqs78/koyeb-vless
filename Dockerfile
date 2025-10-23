# 使用包含完整环境的基础镜像
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

# 设置执行权限
RUN chmod +x /app/start.sh

# 暴露端口
EXPOSE 8000

# 使用启动脚本
CMD ["/app/start.sh"]
