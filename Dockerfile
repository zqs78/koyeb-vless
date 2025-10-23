FROM alpine:latest

RUN apk update && apk add --no-cache \
    curl \
    unzip \
    libcap

# 安装xray-core
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm -rf xray.zip geoip.dat geosite.dat

# 赋予Xray绑定低端口权限
RUN setcap 'cap_net_bind_service=+ep' /usr/local/bin/xray

WORKDIR /app
COPY . /app/

EXPOSE 443

CMD ["/app/start.sh"]
