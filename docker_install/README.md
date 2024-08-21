# Docker 和 Docker Compose 的安装与卸载

本章介绍 Docker 和 Docker Compose 的安装与卸载。

> 本章内容的经验基于笔者之前使用的 ubuntu 20.04 系统，不确定更高版本是否可用。

- [Docker 和 Docker Compose 的安装与卸载](#docker-和-docker-compose-的安装与卸载)
  - [Docker和Docker Compose 安装:](#docker和docker-compose-安装)
  - [安装Docker Compose 1.25.1版本:](#安装docker-compose-1251版本)
    - [docker-compose --version无法使用的解决方案:](#docker-compose---version无法使用的解决方案)
  - [Docker Compose V2安装:](#docker-compose-v2安装)
    - [1. 确保 Docker 已经安装:](#1-确保-docker-已经安装)
    - [2. 安装 Docker Compose 插件:](#2-安装-docker-compose-插件)
    - [3. 验证安装:](#3-验证安装)
  - [Docker指令:](#docker指令)
    - [查看Docker版本:](#查看docker版本)
    - [查看Docker Compose版本的指令如下:](#查看docker-compose版本的指令如下)
    - [检查 Docker 服务的状态(按q键退出检查状态):](#检查-docker-服务的状态按q键退出检查状态)
    - [启动 Docker 服务:](#启动-docker-服务)
    - [将 Docker 添加到启动项，以确保在系统重新启动时 Docker 会自动启动：](#将-docker-添加到启动项以确保在系统重新启动时-docker-会自动启动)
    - [查看本地镜像库所有docker镜像:](#查看本地镜像库所有docker镜像)
  - [卸载Docker Compose:](#卸载docker-compose)
  - [K8s介绍:](#k8s介绍)


## Docker和Docker Compose 安装:

1. 更新包列表:

```bash
sudo apt update
```

2. 安装依赖包，以便可以通过 HTTPS 使用仓库:

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

3. 添加 Docker 官方 GPG 密钥:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

如果由于网络限制上述指令执行失败，可以使用清华源下载GPG密钥:

```bash
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4. 添加 Docker 官方仓库:

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

如果由于网络限制上述指令执行失败，可以添加清华大学的 Docker 软件源：

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. 更新包列表:

```bash
sudo apt update
```

6. 安装 Docker 和 Docker Compose:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose
```

以笔者系统(Ubuntu 18.4)为例，运行上述代码后安装的docker版本为`Docker version 24.0.2, build cb74dfc`，安装的docker compose版本为`docker-compose version 1.17.1, build unknown`。<br>


🚨🚨🚨如果你只想要安装 Docker 而不想安装 Docker Compose，你可以从上述命令中移除`docker-compose`。以下是修改后的命令：<br>

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

这条命令将只会为你安装 Docker 而不包括 Docker Compose。<br>

## 安装Docker Compose 1.25.1版本:

在某些情况下，你可能想要安装不同版本的Docker Compose，此时你可以参考以下指令:<br>

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

运行上述指令后，终端输入`docker-compose --version`将显示以下内容:<br>

```bash
docker-compose version 1.25.1, build a82fef07
```

### docker-compose --version无法使用的解决方案:

如果你终端使用`docker-compose --version`显示如下内容:<br>

```log
(base) root@iZ2zea5v77oawjy2qz7cxxx:/usr/local/bin# docker-compose --version
-bash: /usr/bin/docker-compose: No such file or directory
```

且`/usr/local/bin`目录下的内容有`docker-compose`文件:<br>

```log
(base) root@iZ2zea5v77oawjy2qz7cxxx:/usr/local/bin# ll
total 16676
drwxr-xr-x  2 root root     4096 Oct 27 17:41 ./
drwxr-xr-x 12 root root     4096 Aug  9 10:22 ../
-rwxr-xr-x  1 root root      399 May 15 17:06 cloud-id*
-rwxr-xr-x  1 root root      403 May 15 17:06 cloud-init*
-rwxr-xr-x  1 root root     2108 May 15 17:06 cloud-init-per*
-rwxr-xr-x  1 root root 17032648 Oct 27 17:44 docker-compose*
-rwxr-xr-x  1 root root     1003 May 15 17:06 jsondiff*
-rwxr-xr-x  1 root root     3858 May 15 17:06 jsonpatch*
-rwxr-xr-x  1 root root     1837 May 15 17:06 jsonpointer*
-rwxr-xr-x  1 root root      397 May 15 17:06 jsonschema*
-rwxr-xr-x  1 root root      424 May 15 17:06 normalizer*
```

需要首先检查环境变量是否配置:<br>

```bash
echo $PATH
```

如果没有，需要将`/usr/local/bin`添加至`~/.bashrc` 文件的末尾（对于bash用户）或 `~/.zshrc` （如果你使用zsh）。<br>

> `/usr/local/bin`是按照笔者上方提供的指令安装docker compose的路径。

如果环境变量显示已经有`/usr/local/bin`，那么你可以在终端运行以下指令，用来清除bash的内部命令查找缓存。<br>

```bash
hash -r
docker-compose --version
```

现在大概率已经成功了，会出现这个问题是因为，你之前在不同的位置有 `docker-compose` 的版本，并且bash已经缓存了这个命令的位置。<br>

使用 `hash -r` 来清除缓存是一个有用的技巧，特别是在安装、移动或更改可执行文件的路径时。<br>


## Docker Compose V2安装:

要在 Ubuntu 20.04 上安装 Docker Compose 并准备使用 `sudo docker compose up -d` 命令，你需要先安装 Docker Compose V2，因为在 V2 版本中，`docker-compose` 命令已经集成到 Docker CLI 中，直接用 `docker compose` （没有连字符）来调用。<br>

下面是安装 Docker Compose V2 的步骤：<br>

### 1. 确保 Docker 已经安装:

Docker Compose V2 是 Docker 的一部分，所以你需要先安装 Docker。如果还未安装 Docker，可以运行以下命令来安装：<br>

```bash
sudo apt update
sudo apt install docker.io
```

### 2. 安装 Docker Compose 插件:

使用以下命令安装 Docker Compose V2 作为 Docker 的插件:<br>

```bash
sudo mkdir -p ~/.docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
sudo chmod +x ~/.docker/cli-plugins/docker-compose
```

这些命令从 Docker 的 GitHub 仓库下载最新的 Docker Compose V2 二进制文件到适当的位置，并使其可执行。<br>

终端显示:<br>

```log
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 25.2M  100 25.2M    0     0  56057      0  0:07:52  0:07:52 --:--:-- 1591k
```

### 3. 验证安装:

安装完成后，你可以通过以下命令来检查版本，确认安装是否成功:<br>

```bash
docker compose version
```

终端显示:<br>

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/Pytool_Code# docker compose version
Docker Compose version v2.4.1
```

完成这些步骤后，你就可以使用 `docker compose up -d` 命令来启动你的服务了。<br>


## Docker指令:

现在Docker 和 Docker Compose已经安装好了，下面介绍一些工作中常用的Docker相关指令。<br>

### 查看Docker版本:

```bash
docker --version
```

终端显示如下信息:<br>

```log
Docker version 24.0.2, build cb74dfc
```

### 查看Docker Compose版本的指令如下:

```bash
docker-compose --version
```

终端显示如下信息:<br>

```log
docker-compose version 1.17.1, build unknown
```

### 检查 Docker 服务的状态(按q键退出检查状态):

```bash
sudo systemctl status docker
```

如果 Docker 服务正在运行，你将看到类似如下的输出:<br>

```log
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2023-10-27 16:19:38 CST; 6min ago
     Docs: https://docs.docker.com
 Main PID: 3089 (dockerd)
    Tasks: 11
   CGroup: /system.slice/docker.service
           └─3089 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

Oct 27 16:19:37 iZ2zea5v77oawjy2qz7cxxx systemd[1]: Starting Docker Application Container Engine...
Oct 27 16:19:37 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:37.206729952+08:00" level=info msg="Starting up"
Oct 27 16:19:37 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:37.208940722+08:00" level=info msg="detected 127.0.0.5
Oct 27 16:19:37 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:37.525467345+08:00" level=info msg="Loading containers
Oct 27 16:19:38 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:38.200223894+08:00" level=info msg="Loading containers
Oct 27 16:19:38 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:38.282641593+08:00" level=warning msg="WARNING: No swa
Oct 27 16:19:38 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:38.283251872+08:00" level=info msg="Docker daemon" com
Oct 27 16:19:38 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:38.283552530+08:00" level=info msg="Daemon has complet
Oct 27 16:19:38 iZ2zea5v77oawjy2qz7cxxx dockerd[3089]: time="2023-10-27T16:19:38.385243114+08:00" level=info msg="API listen on /run
Oct 27 16:19:38 iZ2zea5v77oawjy2qz7cxxx systemd[1]: Started Docker Application Container Engine.
lines 1-19/19 (END)
```

### 启动 Docker 服务:

如果你的Docker服务没有启动，可以运行一下指令启动Docker服务:<br>

```bash
sudo systemctl start docker
```

### 将 Docker 添加到启动项，以确保在系统重新启动时 Docker 会自动启动：

```bash
sudo systemctl enable docker
```

终端显示:<br>

```log
Synchronizing state of docker.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable docker
```

### 查看本地镜像库所有docker镜像:

```bash
sudo docker images
```

终端显示:<br>

| REPOSITORY          | TAG                          | IMAGE ID       | CREATED         | SIZE        |
|---------------------|------------------------------|----------------|-----------------|-------------|
| milvusdb/milvus     | v2.3.2                       | 4b6c62c2b5f8   | 3 weeks ago     | 868MB       |
| minio/minio         | RELEASE.2023-03-20T20-16-18Z | 400c20c8aac0   | 8 months ago    | 252MB       |
| quay.io/coreos/etcd | v3.5.5                       | 673f29d03de9   | 14 months ago   | 182MB       |


## 卸载Docker Compose:

```bash
sudo apt remove docker-compose
```

## K8s介绍:

Kubernetes（简称K8s）不是一个容器，而是一个开源的容器编排系统，用于自动化部署、扩展和管理容器化应用程序。它提供了一个平台，使得您可以方便地管理和调度位于物理或虚拟机上的容器。Kubernetes 使得运行和管理跨多个容器（如Docker或rkt等）的应用程序变得更加简单高效。<br>

简单来说，如果把容器比作轿车，那么Kubernetes就像是交通管理系统，负责指挥和调度这些车辆在道路上高效安全地行驶。<br>