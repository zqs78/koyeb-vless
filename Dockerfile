FROM debian:bullseye-slim

# 安装基础工具
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 检测架构并下载正确的 Xray 版本
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget -q https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-64.zip -O xray.zip; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget -q https://github.com/XTLS/Xray-core/releases/download/v1.8.4/Xray-linux-arm64-v8a.zip -O xray.zip; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi

# 解压并安装 Xray
RUN unzip -q xray.zip && \
    rm xray.zip && \
    chmod +x xray && \
    mv xray /usr/local/bin/ && \
    ls -la /usr/local/bin/xray  # 验证文件存在

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
