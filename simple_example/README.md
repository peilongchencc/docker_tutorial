# 简单示例
- [简单示例](#简单示例)
  - [构建 Docker 镜像](#构建-docker-镜像)
  - [运行 Docker 容器:](#运行-docker-容器)
  - [访问 FastAPI 应用:](#访问-fastapi-应用)
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


## 访问 FastAPI 应用:

运行容器后，打开浏览器并访问 `http://localhost:8848/`，你应该能看到返回的 JSON 响应:`{"message": "Hello, Docker with Loguru!"}`。


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