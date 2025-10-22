FROM alpine:latest

# 安装基础工具
RUN apk update && apk add --no-cache \
    wget \
    unzip \
    python3 \
    py3-pip \
    ca-certificates

# 下载并安装 Xray（使用官方最新版本）
RUN wget -q -O /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip -q /tmp/xray.zip -d /tmp/ && \
    mv /tmp/xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm -rf /tmp/*

# 验证安装
RUN ls -la /usr/local/bin/xray && /usr/local/bin/xray version

# 创建工作目录
WORKDIR /app

# 复制文件
COPY . .

# 安装Python依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 创建配置目录
RUN mkdir -p /etc/xray

# 设置执行权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 33333

# 启动命令
CMD ["./start.sh"]
