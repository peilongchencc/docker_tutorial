# 简单示例
- [简单示例](#简单示例)
  - [构建 Docker 镜像](#构建-docker-镜像)
  - [详细构建过程(可选):](#详细构建过程可选)
  - [运行 Docker 容器:](#运行-docker-容器)
  - [查看容器状态:](#查看容器状态)
  - [小技巧:](#小技巧)
  - [容器效果测试:](#容器效果测试)
    - [测试根路径 (`/`):](#测试根路径-)
    - [测试 GET 请求 (`/items/{item_id}`):](#测试-get-请求-itemsitem_id)
    - [测试 POST 请求 (`/items/`):](#测试-post-请求-items)
  - [日志查看:](#日志查看)
  - [存储位置:](#存储位置)
  - [docker compose的作用:](#docker-compose的作用)
  - [附录:构建指令拓展(可选)](#附录构建指令拓展可选)
    - [镜像标签（Tag）的概念](#镜像标签tag的概念)
    - [标签的结构](#标签的结构)
    - [举例说明](#举例说明)
    - [多个标签的使用场景:](#多个标签的使用场景)
    - [如何使用带标签的镜像](#如何使用带标签的镜像)
    - [总结](#总结)
  - [附录:Docker拉取失败解决方案](#附录docker拉取失败解决方案)
    - [查看docker版本(可选):](#查看docker版本可选)
    - [方案一:为 Docker 配置代理](#方案一为-docker-配置代理)
    - [方案二:配置 Docker 镜像加速器](#方案二配置-docker-镜像加速器)
    - [方案三: 如果只是pip问题，可以配置pip源](#方案三-如果只是pip问题可以配置pip源)
  - [附录:docker容器指令](#附录docker容器指令)
    - [列出当前正在运行的容器:](#列出当前正在运行的容器)
    - [显示所有容器，包括已经停止的容器:](#显示所有容器包括已经停止的容器)
    - [关闭/删除容器:](#关闭删除容器)


## 构建 Docker 镜像

构建 Docker 镜像的命令如下:

```bash
docker build -t my-fastapi-app .
```

**解释**: 

- `docker build` 是构建镜像的命令。

- `-t my-fastapi-app` 为镜像指定了标签(tag)（名称），你可以根据需要替换。

    - `-t` 是 `--tag` 的简写，名称可以是随意起的，但最好是有意义的名称。

- `.` 表示 Dockerfile 所在的目录。

运行该命令后，Docker 会按照 `Dockerfile` 中的指令逐步构建镜像。每个指令都会生成一个层（layer），这样可以更快地构建和更新镜像。


## 详细构建过程(可选):

如果你想了解详细构建过程，可以查看下列内容。如果不感兴趣，可以跳过本节。

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker build -t my-fastapi-app .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  11.78kB
Step 1/6 : FROM python:3.11-slim
 ---> 10f461201cdb
Step 2/6 : WORKDIR /app
 ---> Using cache
 ---> 03da3981c191
Step 3/6 : COPY . .
 ---> cb9a11bbe7bd
Step 4/6 : RUN python -m venv docker_example &&     . docker_example/bin/activate &&     pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ &&     pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r requirements.txt
 ---> Running in 80a73ee7b65a
Writing to /root/.config/pip/pip.conf
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Requirement already satisfied: pip in ./docker_example/lib/python3.11/site-packages (24.0)
Collecting pip
  Downloading https://mirrors.aliyun.com/pypi/packages/d4/55/90db48d85f7689ec6f81c0db0622d704306c5284850383c090e6c7195a5c/pip-24.2-py3-none-any.whl (1.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 323.9 kB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-24.2
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting fastapi (from -r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/39/b0/0981f9eb5884245ed6678af234f2cbcd40f44570718caddc0360bdb4015d/fastapi-0.112.1-py3-none-any.whl (93 kB)
Collecting uvicorn (from -r requirements.txt (line 2))
  Downloading https://mirrors.aliyun.com/pypi/packages/f5/8e/cdc7d6263db313030e4c257dd5ba3909ebc4e4fb53ad62d5f09b1a2f5458/uvicorn-0.30.6-py3-none-any.whl (62 kB)
Collecting loguru (from -r requirements.txt (line 3))
  Downloading https://mirrors.aliyun.com/pypi/packages/03/0a/4f6fed21aa246c6b49b561ca55facacc2a44b87d65b8b92362a8e99ba202/loguru-0.7.2-py3-none-any.whl (62 kB)
Collecting starlette<0.39.0,>=0.37.2 (from fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/c1/60/d976da9998e4f4a99e297cda09d61ce305919ea94cbeeb476dba4fece098/starlette-0.38.2-py3-none-any.whl (72 kB)
Collecting pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4 (from fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/1f/fa/b7f815b8c9ad021c07f88875b601222ef5e70619391ade4a49234d12d278/pydantic-2.8.2-py3-none-any.whl (423 kB)
Collecting typing-extensions>=4.8.0 (from fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/26/9f/ad63fc0248c5379346306f8668cda6e2e2e9c95e01216d2b8ffd9ff037d0/typing_extensions-4.12.2-py3-none-any.whl (37 kB)
Collecting click>=7.0 (from uvicorn->-r requirements.txt (line 2))
  Downloading https://mirrors.aliyun.com/pypi/packages/00/2e/d53fa4befbf2cfa713304affc7ca780ce4fc1fd8710527771b58311a3229/click-8.1.7-py3-none-any.whl (97 kB)
Collecting h11>=0.8 (from uvicorn->-r requirements.txt (line 2))
  Downloading https://mirrors.aliyun.com/pypi/packages/95/04/ff642e65ad6b90db43e668d70ffb6736436c7ce41fcc549f4e9472234127/h11-0.14.0-py3-none-any.whl (58 kB)
Collecting annotated-types>=0.4.0 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/78/b6/6307fbef88d9b5ee7421e68d78a9f162e0da4900bc5f5793f6d3d0e34fb8/annotated_types-0.7.0-py3-none-any.whl (13 kB)
Collecting pydantic-core==2.20.1 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/3c/ae/fc99ce1ba791c9e9d1dee04ce80eef1dae5b25b27e3fc8e19f4e3f1348bf/pydantic_core-2.20.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 315.6 kB/s eta 0:00:00
Collecting anyio<5,>=3.4.0 (from starlette<0.39.0,>=0.37.2->fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/7b/a2/10639a79341f6c019dedc95bd48a4928eed9f1d1197f4c04f546fc7ae0ff/anyio-4.4.0-py3-none-any.whl (86 kB)
Collecting idna>=2.8 (from anyio<5,>=3.4.0->starlette<0.39.0,>=0.37.2->fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/e5/3e/741d8c82801c347547f8a2a06aa57dbb1992be9e948df2ea0eda2c8b79e8/idna-3.7-py3-none-any.whl (66 kB)
Collecting sniffio>=1.1 (from anyio<5,>=3.4.0->starlette<0.39.0,>=0.37.2->fastapi->-r requirements.txt (line 1))
  Downloading https://mirrors.aliyun.com/pypi/packages/e9/44/75a9c9421471a6c4805dbf2356f7c181a29c1879239abab1ea2cc8f38b40/sniffio-1.3.1-py3-none-any.whl (10 kB)
Installing collected packages: typing-extensions, sniffio, loguru, idna, h11, click, annotated-types, uvicorn, pydantic-core, anyio, starlette, pydantic, fastapi
Successfully installed annotated-types-0.7.0 anyio-4.4.0 click-8.1.7 fastapi-0.112.1 h11-0.14.0 idna-3.7 loguru-0.7.2 pydantic-2.8.2 pydantic-core-2.20.1 sniffio-1.3.1 starlette-0.38.2 typing-extensions-4.12.2 uvicorn-0.30.6
Removing intermediate container 80a73ee7b65a
 ---> 4d32337ee721
Step 5/6 : EXPOSE 8848
 ---> Running in ac5c62bdbc5a
Removing intermediate container ac5c62bdbc5a
 ---> a7b0d53fcfd2
Step 6/6 : CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8848", "--log-level", "info"]
 ---> Running in 8bbb351acf7d
Removing intermediate container 8bbb351acf7d
 ---> 55e1f853a63e
Successfully built 55e1f853a63e
Successfully tagged my-fastapi-app:latest
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example#
```


## 运行 Docker 容器:

一旦镜像构建完成，你可以使用以下命令运行 Docker 容器:

```bash
docker run -d -p 8848:8848 my-fastapi-app
```

**解释**:

- `docker run` 是运行容器的命令。

- `-d` 表示后台运行容器（detached mode）。

- `-p 8848:8848` 将容器的 `8848` 端口映射到宿主机的 `8848` 端口。这样你可以在宿主机通过 `localhost:8848` 访问应用程序。

- `my-fastapi-app` 是你构建的镜像的名称。


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


## 小技巧:

🌈启动 docker 容器时可以参考以下指令，自己为容器指定一个名称(例如 my-fastapi-app)，方便管理:

```bash
docker run -d -p 8848:8848 --name my-fastapi-app my-fastapi-app
```

终端效果:

```log
指定前:

(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker run -d -p 8848:8848 my-fastapi-app
6cb8e1d416fb5430a798802bf837d29d5b6339d65ffaacd41680458981756096
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                       NAMES
6cb8e1d416fb   my-fastapi-app   "/bin/bash -c '. doc…"   8 seconds ago   Up 7 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   fervent_murdock

指定后:

(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker run -d -p 8848:8848 --name my-fastapi-app my-fastapi-app
75351a8cb88e84298498e0f8a44232969971acf7e9100d227a4feb331a6112f2
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
75351a8cb88e   my-fastapi-app   "/bin/bash -c '. doc…"   22 seconds ago   Up 20 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   my-fastapi-app
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


## 日志查看:

## 存储位置:

## docker compose的作用:


## 附录:构建指令拓展(可选)

在 Docker 中，`:` 是一种分隔符，可以用于指定镜像的**标签**（Tag）。镜像标签通常用来标识不同的版本或变体。例如:

```bash
docker build -t fastapi-demo:v1 .
```

让我详细解释下这种用法:

### 镜像标签（Tag）的概念

镜像标签是 Docker 镜像名称的一部分，位于镜像名称的后面，用冒号（`:`）分隔。例如，`fastapi-demo:v1` 中的 `v1` 就是一个标签。它常用于表示版本号或不同的构建变体。

### 标签的结构

```bash
<镜像名称>:<标签>
```

- **镜像名称**:可以是任意合法名称，表示你构建的应用程序或服务的名称。

- **标签**:用来描述该镜像的特定版本、环境或状态。默认情况下，如果你不指定标签，Docker 会使用 `latest` 标签。

### 举例说明

1. `fastapi-demo:v1`

- **解释**:这表示一个名为 `fastapi-demo` 的镜像，并且它的标签是 `v1`。通常用于表示第一个版本。

2. `fastapi-demo:production`

- **解释**:这里的标签是 `production`，表示这个镜像适用于生产环境。你可以有多个标签来标记不同环境或用途，比如 `development`、`staging` 等。

3. `fastapi-demo:latest`

- **解释**:`latest` 是 Docker 的默认标签。如果你不指定标签，Docker 就会使用 `latest` 作为默认标签。例如，`fastapi-demo` 实际上是 `fastapi-demo:latest` 的简写。

### 多个标签的使用场景:

通过不同的标签，你可以管理相同应用程序的不同版本。例如:

```bash
docker build -t fastapi-demo:v1 .
docker build -t fastapi-demo:v2 .
docker build -t fastapi-demo:latest .
```

这里，你创建了三个不同的镜像:

- `fastapi-demo:v1`（版本 1）

- `fastapi-demo:v2`（版本 2）

- `fastapi-demo:latest`（最新版本）

### 如何使用带标签的镜像

当你运行一个带标签的镜像时，可以直接指定标签:

```bash
docker run -d -p 8848:8848 fastapi-demo:v1
```

这将运行 `v1` 标签对应的镜像。

### 总结

Docker 中的标签机制是非常灵活和有用的。通过使用 `:` 来指定标签，你可以方便地管理同一个应用的不同版本或环境。标签使得在开发、测试、生产等不同阶段部署镜像变得更直观和容易。


## 附录:Docker拉取失败解决方案

如果你运行 `docker build -t my-fastapi-app .` 后，显示下列内容:

```log
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  8.704kB
Step 1/6 : FROM python:3.11-slim
3.11-slim: Pulling from library/python
e4fff0779e6d: Retrying in 1 second 
d97016d0706d: Retrying in 1 second 
53db1713e5d9: Retrying in 1 second 
a8cd795d9ccb: Waiting 
de3ba92de392: Waiting 
error pulling image configuration: download failed after attempts=6: dial tcp 199.59.148.202:443: i/o timeout
```

这与中国的网络环境有关，可以选择 **临时开启代理** 或 **使用国内的 Docker 镜像加速器** (例如阿里云Docker镜像加速器)。

### 查看docker版本(可选):

终端输入以下指令将显示 Docker 客户端的版本:

```bash
docker --version
```

终端将显示类似以下信息:

```log
Docker version 24.0.5, build 24.0.5-0ubuntu1~22.04.1
```


### 方案一:为 Docker 配置代理

以笔者使用的 ubuntu 22.04 为例，Ubuntu 22.04 通常使用 systemd 来管理服务，因此需要在 Docker 的 systemd 配置中设置代理：:

1. **创建或编辑 Docker 的代理配置文件**：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```

2. **添加代理设置**：

```conf
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,::1"
```

如果你的代理需要认证，可以使用以下格式：

```conf
Environment="HTTP_PROXY=http://username:password@127.0.0.1:7890"
Environment="HTTPS_PROXY=http://username:password@127.0.0.1:7890"
```

3. **重新加载 systemd 并重启 Docker**：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

4. **验证代理配置是否生效**：

```bash
sudo systemctl show --property=Environment docker
```

### 方案二:配置 Docker 镜像加速器

如果你在中国大陆，配置 Docker 镜像加速器可以显著加快镜像下载速度：

1. **添加 Docker 镜像加速器地址**到 `daemon.json`：

示例（使用阿里云的镜像加速器）：

```json
{
    "registry-mirrors": ["https://9r0ctibg.mirror.aliyuncs.com"]
}
```

2. **加载修改后的配置**:

```bash
sudo systemctl daemon-reload
```

3. **保存文件并重启 Docker**：

```bash
sudo systemctl restart docker
```


### 方案三: 如果只是pip问题，可以配置pip源

将 `Dockerfile` 中的pip源改为国内源(例如阿里源)，示例代码如下:

```bash
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```


## 附录:docker容器指令

### 列出当前正在运行的容器:

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

### 显示所有容器，包括已经停止的容器:

```bash
docker ps -a
```

🚨可有效删除那些你构建成功，但启动失败的容器。

### 关闭/删除容器:

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