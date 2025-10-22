FROM debian:bullseye-slim

# 安装必要的工具
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Xray-core
RUN wget -q https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip \
    && unzip -q Xray-linux-64.zip \
    && rm Xray-linux-64.zip \
    && chmod +x xray

# 创建配置目录
RUN mkdir -p /etc/xray

# 复制配置文件
COPY config.json /etc/xray/config.json

# 创建非root用户运行
RUN groupadd -r xray && useradd -r -g xray xray
RUN chown -R xray:xray /etc/xray

# 暴露端口
EXPOSE 33333

# 启动命令
USER xray
CMD ["./xray", "run", "-config", "/etc/xray/config.json"]
