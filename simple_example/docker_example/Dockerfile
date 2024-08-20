# 使用官方的Python基础镜像(FROM 指令指定了基础镜像，python:3.11-slim 是一个精简版的 Python 3.11 镜像，包含了运行 Python 的必要文件，去掉了不必要的部分，体积较小。)
FROM python:3.11-slim

# 设置 Docker 容器内部的工作目录。这个工作目录是所有后续命令（如 COPY、RUN、CMD 等）的相对路径基准。
# 如果指定的目录（如 /app）不存在，WORKDIR 会自动创建它。
# 一般情况下，为了保持容器内部的结构简洁，推荐使用较短的路径如 /app。
WORKDIR /app

# 将当前目录(Dockerfile 所在的目录)的内容复制到 Docker 容器的 /app 目录下
# 当你执行 COPY 命令时，比如 COPY . .，它的含义是：
# 第一个 .：表示 Dockerfile 所在的目录（/data/docker_example）内的所有内容。
# 第二个 .：表示将这些内容复制到容器内部的当前工作目录（由 WORKDIR /app 指定）。
COPY . .

# RUN 指令执行 shell 命令
# 创建虚拟环境并激活，然后安装依赖
# 安装依赖时 --no-cache-dir 参数可以减少 Docker 镜像的体积。
RUN python -m venv docker_example && \
    . docker_example/bin/activate && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# EXPOSE 指令告诉 Docker 容器应用程序将在 8848 端口上监听。这个端口将映射到宿主机，使得应用可以从外部访问。
# 暴露端口 8848
EXPOSE 8848

# 配置 Uvicorn 运行 FastAPI 应用，日志级别为
CMD ["/bin/bash", "-c", ". docker_example/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8848 --log-level info"]