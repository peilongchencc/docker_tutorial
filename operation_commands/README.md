# docker容器操作指令

本章介绍 docker 容器操作指令。
- [docker容器操作指令](#docker容器操作指令)
  - [列出当前正在运行的容器:](#列出当前正在运行的容器)
  - [显示所有容器，包括已经停止的容器:](#显示所有容器包括已经停止的容器)
  - [关闭/删除容器:](#关闭删除容器)
  - [查看容器大小:](#查看容器大小)
    - [解释：](#解释)
    - [Docker 分层文件系统:](#docker-分层文件系统)


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


## 查看容器大小:

要查看一个 Docker 容器的大小，你可以终端使用下列指令：

```bash
docker ps -s
```

在输出中，`SIZE` 列表示容器的大小，其中包括：

- **Virtual Size**: 基础镜像和该容器所有层的总和。

- **Size**: 该容器的可写层所占用的空间，即容器启动后生成的数据。

例如:

```bash
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/containers/dec75f4de335183a9323cd1d91e5167d33249ef0400d182c6bbf54eefa8dfbf2# docker ps -s
CONTAINER ID   IMAGE            COMMAND                  CREATED        STATUS        PORTS                                       NAMES         SIZE
dec75f4de335   my-fastapi-app   "/bin/bash -c '. doc…"   16 hours ago   Up 16 hours   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   jolly_cohen   139kB (virtual 170MB)
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/containers/dec75f4de335183a9323cd1d91e5167d33249ef0400d182c6bbf54eefa8dfbf2# 
```

🚨注意:

容器的总大小就是 `170MB`，**不需要再加上 `139kB`**。

### 解释：

- **170MB (Virtual Size)**: 这是容器的**总体大小**，包括基础镜像和容器的可写层(`139kB`)。

- **139kB (Size)**: 这是容器的**可写层大小**，表示容器启动后发生的更改或新增数据的大小。


### Docker 分层文件系统:

我简单解释下 Docker 分层文件系统，帮助你理解什么是可写入层:

Docker 容器基于镜像运行，而镜像本身是由多个只读层组成的。当你启动容器时，Docker 会在这些只读层之上创建一个**可写层（Writable Layer）**。这个可写层是容器独有的，可以用来存储在容器运行时产生的数据。

关键点：

1. **只读层**（Read-Only Layers）：

   - 这些层包含了你的应用程序代码、依赖库、操作系统文件等。在容器运行时，这些层是不可修改的，所有的代码和数据都是从这些层读取的。

2. **可写层**（Writable Layer）：

   - 这是容器独有的层，当容器运行时，所有的文件变化（包括新增、修改或删除）都发生在这一层。例如，如果容器在运行时创建了新文件、修改了现有文件、生成了日志或其他数据，这些更改都被写入可写层。

举例说明：

假设你有一个 Python 应用程序：

- 你在 Dockerfile 中将代码拷贝到 `/app` 目录，并构建镜像。这时，代码在只读层中。

- 你启动容器，应用程序开始运行并写入一些日志文件到 `/app/logs` 目录。这些日志文件就存储在可写层中。

在这种情况下：

- 代码的大小位于只读层，不会影响容器的可写层大小。

- 日志文件等在运行时生成的数据占用可写层空间，所以 `docker ps -s` 中显示的 `139kB` 是这些运行时数据的大小，而不是你的代码的大小。

总结:

“容器的可写层的大小”反映了容器运行时产生的所有新增或修改的数据的大小，而不仅仅是代码的大小。代码通常位于只读层中，除非你在容器运行时修改了它们。