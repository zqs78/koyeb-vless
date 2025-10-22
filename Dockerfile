FROM debian:bullseye-slim

# 安装基础工具
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 下载 Xray
RUN wget -q https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip \
    && unzip -q Xray-linux-64.zip \
    && ls -la
    && rm Xray-linux-64.zip \
    && chmod +x xray \
    && mv xray /usr/local/bin/

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

# 只暴露必要的端口
EXPOSE 33333

# 启动命令
CMD ["./start.sh"]
