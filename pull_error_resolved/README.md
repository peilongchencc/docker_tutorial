# Docker拉取失败解决方案

本章介绍Docker拉取失败的解决方案。

- [Docker拉取失败解决方案](#docker拉取失败解决方案)
  - [情况描述:](#情况描述)
  - [查看docker版本(可选):](#查看docker版本可选)
  - [方案一: 终端临时开启代理](#方案一-终端临时开启代理)
  - [方案二: 为 Docker 配置代理](#方案二-为-docker-配置代理)
    - [1. 创建或编辑 Docker 的代理配置文件：](#1-创建或编辑-docker-的代理配置文件)
    - [2. 添加代理设置：](#2-添加代理设置)
    - [3. 重新加载 systemd 并重启 Docker：](#3-重新加载-systemd-并重启-docker)
    - [4. 验证代理配置是否生效：](#4-验证代理配置是否生效)
  - [方案三:配置 Docker 镜像加速器](#方案三配置-docker-镜像加速器)
    - [1. 添加 Docker 镜像加速器地址到 `daemon.json`：](#1-添加-docker-镜像加速器地址到-daemonjson)
    - [2. 加载修改后的配置:](#2-加载修改后的配置)
    - [3. 保存文件并重启 Docker：](#3-保存文件并重启-docker)
  - [方案四: 如果只是pip问题，可以配置pip源](#方案四-如果只是pip问题可以配置pip源)

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


## 方案一: 终端临时开启代理

临时开启代理测试连接:

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
```

终端输入下列指令测试效果:

```bash
# 注意修改自己的代理端口
curl -I https://www.google.com --proxy http://127.0.0.1:7890
```

> [!CAUTION]
> ping 命令使用 ICMP 协议，而不是 HTTP/HTTPS 协议，因此它不会通过 http_proxy 或 https_proxy 环境变量指定的代理进行通信。因此，即使代理设置正确，ping 命令仍会绕过代理，直接访问网络。所以不要使用 `ping google.com` 指令测试。

终端将显示类似以下内容(HTTP 200 状态码表示连接已建立，并且接收到了响应):

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example# curl -I https://www.google.com --proxy http://127.0.0.1:7890
HTTP/1.1 200 Connection established

HTTP/2 200 
content-type: text/html; charset=ISO-8859-1
content-security-policy-report-only: object-src 'none';base-uri 'self';script-src 'nonce-ywoCqdn2Rdp4v9XZ6U2YQQ' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
p3p: CP="This is not a P3P policy! See g.co/p3phelp for more info."
date: Mon, 19 Aug 2024 05:56:38 GMT
server: gws
x-xss-protection: 0
x-frame-options: SAMEORIGIN
expires: Mon, 19 Aug 2024 05:56:38 GMT
cache-control: private
set-cookie: AEC=AVYB7cqaddgWijgwVn_mJlAnnBkaieEE43BqhNjSmOK4rzCgY5DGvvFTkQw; expires=Sat, 15-Feb-2025 05:56:38 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
set-cookie: NID=516=lXhyP1QSw882JyvonhhmhLtWcLnyL5_VXiesFhxUR__2Z_OHMEewaKJQse9le4rua6taDROomc66wlktfu8b6mUrJ720OXa1cHbF_tmtng04GwhRs-zky0FFjYe7-kmv7O6qv83a-_M8yF2n4rrvqGe8th4vpQplus0FMZPqJxxhxirSq15IrA; expires=Tue, 18-Feb-2025 05:56:38 GMT; path=/; domain=.google.com; HttpOnly
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000

(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_example#
```


## 方案二: 为 Docker 配置代理

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


## 方案三:配置 Docker 镜像加速器

如果你在中国大陆，配置 Docker 镜像加速器可以显著加快镜像下载速度：

### 1. 添加 Docker 镜像加速器地址到 `daemon.json`：

```bash
vim /etc/docker/daemon.json
```

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


## 方案四: 如果只是pip问题，可以配置pip源

将 `Dockerfile` 中的pip源改为国内源(例如阿里源)，示例代码如下:

```bash
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```
