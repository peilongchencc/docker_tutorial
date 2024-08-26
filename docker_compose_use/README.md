# Docker Compose 的使用

本章以 `LLaMA-Factory` 中docker-cuda的 [docker-compose.yml](https://github.com/hiyouga/LLaMA-Factory/blob/main/docker/docker-cuda/docker-compose.yml) 文件为例，讲解 Docker Compose 的使用。
- [Docker Compose 的使用](#docker-compose-的使用)
  - [LLaMA-Factory中的docker-compose.yml源文件:](#llama-factory中的docker-composeyml源文件)
  - [docker compose指令:](#docker-compose指令)
    - [查看当前所有服务的状态：](#查看当前所有服务的状态)
    - [启动服务：](#启动服务)
    - [调试和开发:](#调试和开发)
    - [查看容器日志:](#查看容器日志)
    - [停止容器（不删除）：](#停止容器不删除)
    - [重新启动已停止的容器：](#重新启动已停止的容器)
    - [停止并删除容器：](#停止并删除容器)
  - [附录:`docker compose up -d`和`docker compose start`区别](#附录docker-compose-up--d和docker-compose-start区别)
    - [1. docker compose up -d](#1-docker-compose-up--d)
    - [2. docker compose start](#2-docker-compose-start)


## LLaMA-Factory中的docker-compose.yml源文件:

```yaml
services:
  llamafactory:
    build:
      dockerfile: ./docker/docker-cuda/Dockerfile  # 指定 Dockerfile 的路径
      context: ../..  # 设置构建上下文为上两级目录
      args:
        INSTALL_BNB: false  # 构建时传递的参数，用于控制是否安装 bitsandbytes
        INSTALL_VLLM: false  # 控制是否安装 vllm
        INSTALL_DEEPSPEED: false  # 控制是否安装 DeepSpeed
        INSTALL_FLASHATTN: false  # 控制是否安装 Flash Attention
        PIP_INDEX: https://pypi.org/simple  # 设置 Python 包的镜像源

    container_name: llamafactory  # 指定容器的名称为 llamafactory

    volumes:
      # 将主机目录映射到容器内部目录，确保数据在容器重启或重建时不丢失
      - ../../hf_cache:/root/.cache/huggingface  # 缓存 Hugging Face 模型数据
      - ../../ms_cache:/root/.cache/modelscope  # 缓存 ModelScope 模型数据
      - ../../data:/app/data  # 应用程序的数据目录
      - ../../output:/app/output  # 应用程序的输出目录

    ports:
      # 将容器的端口映射到主机端口，方便从外部访问服务
      - "7860:7860"  # Gradio 界面
      - "8000:8000"  # API 服务

    ipc: host  # 允许容器与主机共享 IPC 资源（如内存），适合需要大量内存的应用

    tty: true  # 为容器分配一个伪终端，允许交互式操作
    stdin_open: true  # 保持 stdin 打开，允许通过命令行输入

    command: bash  # 容器启动后默认执行的命令，这里设置为进入 bash Shell

    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia  # 指定使用 NVIDIA 驱动
              count: "all"  # 允许使用所有可用的 GPU
              capabilities: [gpu]  # 指定设备的能力为 GPU

    restart: unless-stopped  # 配置容器自动重启，除非手动停止
```


## docker compose指令:

以下指令均在定义了 `docker-compose.yml` 的目录中运行:

### 查看当前所有服务的状态：

```bash
docker compose ps
```

### 启动服务：

```bash
docker compose up -d
```

- 这将以后台模式启动容器服务。

### 调试和开发:

你可以进入容器以调试或手动运行命令：

```bash
docker compose exec llamafactory bash
```

- 进入容器后，可以执行命令查看或修改其行为。

`llamafactory` 对应的是 `docker-compose.yml` 文件中的 `services` 部分下的服务名称，即：

```yaml
services:
  llamafactory:
```

### 查看容器日志:

如果需要查看日志，可以使用:

```bash
docker compose logs -f
```

### 停止容器（不删除）：

```bash
docker compose stop
```

### 重新启动已停止的容器：

```bash
docker compose start
```

### 停止并删除容器：

- 要停止并删除容器，在定义了 `docker-compose.yml` 的目录使用：

```bash
docker compose down
```

- 这将停止容器并删除网络、卷等资源。


## 附录:`docker compose up -d`和`docker compose start`区别

`docker compose up -d` 和 `docker compose start` 是两个常用的 Docker Compose 命令，但它们的作用有所不同。以下是它们的主要区别：

### 1. docker compose up -d

- 功能: `docker compose up` 是一个 **创建并启动** 容器的命令。
- 作用:
  - 构建镜像（如果未构建）并创建容器：如果这是第一次运行，或者 Dockerfile 或 `docker-compose.yml` 文件有更改，它会根据定义构建镜像。
  - 创建并启动容器：如果容器不存在，它将创建并启动容器。
  - 启动所有相关的网络和卷。
- `-d` 选项: 表示以“后台模式”运行容器，不会在终端中输出日志。
- 适用场景: 用于启动整个应用程序栈。无论容器是否已经存在，都会尝试启动所有相关服务。

```bash
docker compose up -d
```

### 2. docker compose start

- 功能: `docker compose start` 是一个用于启动已经停止的容器的命令。
- 作用:
  - 仅启动已经存在的、之前已创建但已停止的容器。
  - 不会重新构建镜像、创建新容器或重新初始化卷和网络。
- 适用场景: 当你已经通过 `docker compose up` 创建并运行了容器，并且之后通过 `docker compose stop` 停止了它们，想再次启动它们时使用这个命令。

```bash
docker compose start
```