# docker容器操作指令

本章介绍 docker 容器操作指令。
- [docker容器操作指令](#docker容器操作指令)
  - [列出当前正在运行的容器:](#列出当前正在运行的容器)
  - [显示所有容器，包括已经停止的容器:](#显示所有容器包括已经停止的容器)
  - [关闭/删除容器:](#关闭删除容器)


## 列出当前正在运行的容器:

```bash
docker ps
```

终端将显示类似以下信息:

```bash
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
75351a8cb88e   my-fastapi-app   "/bin/bash -c '. doc…"   22 seconds ago   Up 20 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   my-fastapi-app
```

- **CONTAINER ID**: 容器的唯一标识符（ID）。
- **IMAGE**: 容器使用的 Docker 镜像名称。
- **COMMAND**: 容器启动时执行的命令。
- **CREATED**: 容器创建的时间。
- **STATUS**: 容器的当前状态。
- **PORTS**: 容器暴露的端口以及对应的宿主机端口映射。
- **NAMES**: Docker 自动生成或用户自定义的容器名称。


## 显示所有容器，包括已经停止的容器:

```bash
docker ps -a
```

🚨可有效删除那些你构建成功，但启动失败的容器。


## 关闭/删除容器:

要关闭/删除容器，跟容器的 `CONTAINER ID` 或 `NAMES` 有关，例如:

- `docker stop <容器ID或名称>` 用于停止容器。
- `docker rm <容器ID或名称>` 用于删除已经停止的容器。
- `docker rm -f <容器ID或名称>` 强制停止并删除容器(相当于一次性完成上述两个操作)。

例如使用容器ID(`CONTAINER ID`):

```bash
docker stop 75351a8cb88e
```

使用容器名称(`NAMES`):

```bash
docker rm -f my-fastapi-app
```