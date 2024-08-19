# Docker拉取失败解决方案

本章介绍Docker拉取失败的解决方案。

- [Docker拉取失败解决方案](#docker拉取失败解决方案)
  - [情况描述:](#情况描述)
  - [查看docker版本(可选):](#查看docker版本可选)
  - [方案一:为 Docker 配置代理](#方案一为-docker-配置代理)
    - [1. 创建或编辑 Docker 的代理配置文件：](#1-创建或编辑-docker-的代理配置文件)
    - [2. 添加代理设置：](#2-添加代理设置)
    - [3. 重新加载 systemd 并重启 Docker：](#3-重新加载-systemd-并重启-docker)
    - [4. 验证代理配置是否生效：](#4-验证代理配置是否生效)
  - [方案二:配置 Docker 镜像加速器](#方案二配置-docker-镜像加速器)
    - [1. 添加 Docker 镜像加速器地址到 `daemon.json`：](#1-添加-docker-镜像加速器地址到-daemonjson)
    - [2. 加载修改后的配置:](#2-加载修改后的配置)
    - [3. 保存文件并重启 Docker：](#3-保存文件并重启-docker)
  - [方案三: 如果只是pip问题，可以配置pip源](#方案三-如果只是pip问题可以配置pip源)

## 情况描述:

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


## 查看docker版本(可选):

终端输入以下指令将显示 Docker 客户端的版本:

```bash
docker --version
```

终端将显示类似以下信息:

```log
Docker version 24.0.5, build 24.0.5-0ubuntu1~22.04.1
```


## 方案一:为 Docker 配置代理

以笔者使用的 ubuntu 22.04 为例，Ubuntu 22.04 通常使用 systemd 来管理服务，因此需要在 Docker 的 systemd 配置中设置代理：:

### 1. 创建或编辑 Docker 的代理配置文件：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```

### 2. 添加代理设置：

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

### 3. 重新加载 systemd 并重启 Docker：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 4. 验证代理配置是否生效：

```bash
sudo systemctl show --property=Environment docker
```


## 方案二:配置 Docker 镜像加速器

如果你在中国大陆，配置 Docker 镜像加速器可以显著加快镜像下载速度：

### 1. 添加 Docker 镜像加速器地址到 `daemon.json`：

示例（使用阿里云的镜像加速器）：

```json
{
    "registry-mirrors": ["https://9r0ctibg.mirror.aliyuncs.com"]
}
```

### 2. 加载修改后的配置:

```bash
sudo systemctl daemon-reload
```

### 3. 保存文件并重启 Docker：

```bash
sudo systemctl restart docker
```


## 方案三: 如果只是pip问题，可以配置pip源

将 `Dockerfile` 中的pip源改为国内源(例如阿里源)，示例代码如下:

```bash
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```
