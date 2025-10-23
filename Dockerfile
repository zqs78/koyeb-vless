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

# 复制您的main.py文件
COPY main.py /app/main.py

# 安装Python依赖（如果有requirements.txt的话）
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# 创建xray运行用户
RUN adduser -D -u 1000 xray

# 切换用户
USER xray

# 暴露端口（根据您的配置调整）
EXPOSE 8080 8443

# 健康检查（使用您原有的main.py）
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 /app/main.py

# 启动命令
CMD ["/usr/local/bin/xray", "run", "-config", "/etc/xray/config.json"]
