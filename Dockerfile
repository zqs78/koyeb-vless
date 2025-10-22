FROM teddysun/xray:latest

# 复制配置文件
COPY config.json /etc/xray/config.json

# 复制健康检查脚本
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# 安装Python3
RUN apk add --no-cache python3 py3-pip

# 安装Python依赖
RUN pip3 install -r /app/requirements.txt

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 33333

# 启动命令（同时运行Xray和健康检查）
CMD sh -c '/etc/xray/xray run -config /etc/xray/config.json & python3 main.py'
