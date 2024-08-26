# 简单示例

本章以的 `simple_example/docker_example` 文件为例，介绍 docker 的简单使用。

- [简单示例](#简单示例)
  - [切换路径:](#切换路径)
  - [构建 Docker 镜像](#构建-docker-镜像)
  - [docker中版本号的使用(可选):](#docker中版本号的使用可选)
    - [标签的结构如下:](#标签的结构如下)
    - [常用版本号示例:](#常用版本号示例)
  - [详细构建过程(可选):](#详细构建过程可选)
  - [运行 Docker 容器:](#运行-docker-容器)
    - [1. 常规启动:](#1-常规启动)
    - [2. 自定义容器名称并启动:](#2-自定义容器名称并启动)
  - [查看容器状态:](#查看容器状态)
  - [容器效果测试:](#容器效果测试)
    - [测试根路径 (`/`):](#测试根路径-)
    - [测试 GET 请求 (`/items/{item_id}`):](#测试-get-请求-itemsitem_id)
    - [测试 POST 请求 (`/items/`):](#测试-post-请求-items)

## 切换路径:

拉取代码后，将终端路径切换到 `simple_example/docker_example` 所在目录，例如:

```bash
cd /data/docker_tutorial/simple_example/docker_example
```


## 构建 Docker 镜像

构建 Docker 镜像的命令如下:

```bash
docker build -t fastapi-demo:v1 .
```

**解释**: 

- `docker build` 这个命令用于根据指定的 Dockerfile 创建一个新的 Docker 镜像。

- `-t fastapi-demo:v1` 为镜像指定了标签(tag)（名称），你可以根据需要替换。
  - `-t` 是 `--tag` 的简写，用于为构建的镜像指定一个标签（Tag）。标签通常由镜像名称和版本组成，这里标签为 `fastapi-demo:v1`。
  - `fastapi-demo` 是镜像的名称，通常表示镜像的用途或项目名称。
  - `v1` 是版本号，用来标识这个镜像的特定版本。用途:通过版本号区分不同的镜像版本。

- `.` 表示 Dockerfile 所在的目录。

运行该命令后，Docker 会按照 `Dockerfile` 中的指令逐步构建镜像。每个指令都会生成一个层（layer），这样可以更快地构建和更新镜像。


## docker中版本号的使用(可选):

镜像标签是 Docker 镜像名称的一部分，位于镜像名称的后面，用冒号（`:`）分隔。例如，`fastapi-demo:v1` 中的 `v1` 就是一个标签，它常用于表示版本号。

### 标签的结构如下:

```bash
<镜像名称>:<标签>
```

- **镜像名称**:可以是任意合法名称，表示你构建的应用程序或服务的名称。

- **标签**:用来描述该镜像的特定版本、环境或状态。默认情况下，如果你不指定标签，Docker 会使用 `latest` 标签。

🔥例如: `docker build -t fastapi-demo .` --等于--> `docker build -t fastapi-demo:latest .`。

### 常用版本号示例:

1. `fastapi-demo:v1`

- **解释**:这表示一个名为 `fastapi-demo` 的镜像，并且它的标签是 `v1`。通常用于表示第一个版本。

2. `fastapi-demo:production`

- **解释**:这里的标签是 `production`，表示这个镜像适用于生产环境。你可以有多个标签来标记不同环境或用途，比如 `development`、`staging` 等。

3. `fastapi-demo:latest`

- **解释**:`latest` 是 Docker 的默认标签。如果你不指定标签，Docker 就会使用 `latest` 作为默认标签。例如，`fastapi-demo` 实际上是 `fastapi-demo:latest` 的简写。


## 详细构建过程(可选):

如果你想了解详细构建过程，可以查看下列内容。如果不感兴趣，可以跳过本节。

```log
docker build -t fastapi-demo:v1 .
DEPRECATED: The legacy builder is deprecated...

Sending build context to Docker daemon  9.728kB
Step 1/6 : FROM python:3.11-slim
 ---> 10f461201cdb
Step 2/6 : WORKDIR /app
 ---> 3d2be49b3c3d
Step 3/6 : COPY . .
 ---> 7b3471f0f66b
Step 4/6 : RUN python -m venv docker_example && \
    . docker_example/bin/activate && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
Successfully installed pip-24.2
Successfully installed fastapi-0.112.2 uvicorn-0.30.6 loguru-0.7.2
 ---> a79ed1c58cf8
Step 5/6 : EXPOSE 8848
 ---> 26323d4ce2fe
Step 6/6 : CMD ["/bin/bash", "-c", ". docker_example/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8848 --log-level info"]
 ---> 4f780f0748eb
Successfully built 4f780f0748eb
Successfully tagged fastapi-demo:v1
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial/simple_example/docker_example#
```


## 运行 Docker 容器:

一旦镜像构建完成，你可以从以下2种方式选择一种运行 Docker 容器:

> 在非 `Dockerfile` 所在目录也能运行。

### 1. 常规启动:

```bash
docker run -d -p 8848:8848 fastapi-demo:v1
```

### 2. 自定义容器名称并启动:

🌈容器指定一个名称可以方便管理，如果你不指定名称，系统后随机生成一个名称("NAMES")。

```bash
docker run -d -p 8848:8848 --name fastapi-demo-container fastapi-demo:v1
```

**解释**:

- `docker run` 是运行容器的命令。

- `-d` 表示后台运行容器（detached mode）。

- `-p 8848:8848` 将容器的 `8848` 端口映射到宿主机的 `8848` 端口。这样你可以在宿主机通过 `localhost:8848` 访问应用程序。

- `--name fastapi-demo-container`(可选，推荐使用): 给容器指定一个名称`fastapi-demo-container`，方便管理。

- `fastapi-demo:v1`: 指定要运行的镜像和标签。

终端显示:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial/simple_example/docker_example# docker run -d -p 8848:8848 fastapi-demo:v1
fa476a55eeb7f8fcfb1d607e663a325f054e4a6583cf7cffba5060f4d7b5c762
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial/simple_example/docker_example# docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                                       NAMES
fa476a55eeb7   fastapi-demo:v1   "/bin/bash -c '. doc…"   4 seconds ago   Up 3 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   beautiful_moser
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial/simple_example/docker_example# docker stop beautiful_moser
beautiful_moser
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial/simple_example/docker_example# docker run -d -p 8848:8848 --name fastapi-demo-container fastapi-demo:v1
10f53c36fb5b624219c116d857efb6da41b515adc5212756d13d889a6b2f5908
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial/simple_example/docker_example# docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                                       NAMES
10f53c36fb5b   fastapi-demo:v1   "/bin/bash -c '. doc…"   4 seconds ago   Up 3 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   fastapi-demo-container
```


## 查看容器状态:

```bash
docker ps
```

终端显示:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker run -d -p 8848:8848 my-fastapi-app
6cb8e1d416fb5430a798802bf837d29d5b6339d65ffaacd41680458981756096
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                       NAMES
6cb8e1d416fb   my-fastapi-app   "/bin/bash -c '. doc…"   8 seconds ago   Up 7 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   fervent_murdock
```


## 容器效果测试:

你已经成功启动了 Docker 容器，并且应用程序正在运行。接下来，你可以使用以下方法来测试你的 FastAPI 接口。

> 本节使用的curl，你也可以使用postman或apifox测试。

### 测试根路径 (`/`):

```bash
curl http://localhost:8848/
```

你应该看到类似于以下的响应：

```json
{"message":"Hello, Docker with Loguru!"}
```

### 测试 GET 请求 (`/items/{item_id}`):

```bash
curl "http://localhost:8848/items/1?q=test"
```

你应该看到类似于以下的响应：

```json
{"item_id":1,"q":"test"}
```

### 测试 POST 请求 (`/items/`):

```bash
curl -X POST "http://localhost:8848/items/" -H "Content-Type: application/json" -d '{"name": "apple", "description": "A juicy fruit", "price": 1.5, "tax": 0.1}'
```

你应该看到类似于以下的响应：

```json
{"item":{"name":"apple","description":"A juicy fruit","price":1.5,"tax":0.1}}
```