FROM debian:bullseye-slim

# 安装必要的工具
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 下载并安装 Xray-core
RUN wget -q https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip \
    && unzip -q Xray-linux-64.zip \
    && rm Xray-linux-64.zip \
    && chmod +x xray

# 创建配置目录
RUN mkdir -p /etc/xray

# 复制配置文件
COPY config.json /etc/xray/config.json
COPY main.py .
COPY start.sh .

# 设置执行权限
RUN chmod +x start.sh

# 暴露端口（VLESS服务和健康检查服务）
EXPOSE 33333 8000

# 启动命令
CMD ["./start.sh"]
