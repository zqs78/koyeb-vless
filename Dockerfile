FROM alpine:latest

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

WORKDIR /app
COPY . /app/

# 使用root用户运行（避免端口权限问题）
USER root

EXPOSE 8000
CMD sh -c "echo '启动Xray服务...' && /usr/local/bin/xray run -config /app/config.json & echo '启动健康检查...' && python3 /app/main.py"
