FROM alpine:latest

RUN apk update && apk add --no-cache \
    python3 \
    curl \
    unzip

# 安装xray-core
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm -rf xray.zip geoip.dat geosite.dat

WORKDIR /app
COPY . /app/

EXPOSE 8000

CMD ["python3", "/app/main.py"]
