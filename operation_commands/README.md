# docker容器操作指令

本章介绍 docker 容器操作指令。
- [docker容器操作指令](#docker容器操作指令)
  - [前言:](#前言)
    - [1. 镜像 (Image)](#1-镜像-image)
    - [2. 容器 (Container)](#2-容器-container)
    - [总结](#总结)
  - [容器操作:](#容器操作)
    - [列出当前正在运行的容器:](#列出当前正在运行的容器)
    - [显示所有容器，包括已经停止的容器:](#显示所有容器包括已经停止的容器)
    - [关闭/删除容器:](#关闭删除容器)
    - [查看容器大小:](#查看容器大小)
      - [解释：](#解释)
      - [Docker 分层文件系统:](#docker-分层文件系统)
  - [镜像操作:](#镜像操作)
    - [查看已拉取的镜像:](#查看已拉取的镜像)
    - [终端示例:](#终端示例)
    - [镜像引用分析:](#镜像引用分析)
    - [镜像和标签的关系](#镜像和标签的关系)
    - [镜像引用分析结论:](#镜像引用分析结论)
    - [删除镜像:](#删除镜像)
    - [如何清理这些 `<none>` 镜像](#如何清理这些-none-镜像)
    - [搜索镜像资源:](#搜索镜像资源)


## 前言:

介绍docker容器操作指令前，我们先理清一下 **"镜像"、"容器"** 的概念:

**镜像** 和 **容器** 是 Docker 中的两个核心概念，但它们的功能和用途不同。理解它们的区别有助于更好地使用 Docker。

### 1. 镜像 (Image)

- 定义：镜像是一个只读的模板，包含了运行应用程序所需的文件系统和内容。镜像可以包含操作系统、应用程序、依赖库和配置文件。
- 用途：镜像是创建容器的基础。你可以把它看作是一个应用程序或服务的“快照”。
- 静态性：镜像是不可变的，一旦创建，内容不会改变。

比喻：镜像就像一个安装程序（例如 `.exe` 文件），包含了应用程序和所有需要的依赖，但它本身并不运行。

### 2. 容器 (Container)

- 定义：容器是镜像的一个实例，它是一个运行时环境，包含了应用程序的所有依赖和代码。🔥容器是通过镜像启动的，并在其中运行一个或多个进程。
- 用途：容器是一个独立运行的环境，可以用来运行应用程序。容器具有隔离性，每个容器在各自独立的环境中运行。
- 动态性：容器是动态的，可以启动、停止、删除。容器的数据和状态会根据运行时的操作而变化。

比喻：容器就像你安装并运行的一个软件实例（如在 Windows 上运行的一个程序），它是基于安装程序（镜像）创建的，并在运行时具有状态。

### 总结

- **镜像**：是静态的、只读的模板，用来创建容器。
- **容器**：是动态的、可运行的实例，是通过镜像创建的。


## 容器操作:

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

### 查看容器大小:

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

#### 解释：

- **170MB (Virtual Size)**: 这是容器的**总体大小**，包括基础镜像和容器的可写层(`139kB`)。

- **139kB (Size)**: 这是容器的**可写层大小**，表示容器启动后发生的更改或新增数据的大小。


#### Docker 分层文件系统:

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


## 镜像操作:

### 查看已拉取的镜像:

🚨记得笔者在 **前言** 说的，容器和镜像是不一样的概念‼️

下列指令可列出本地 Docker 主机上所有可用镜像:

```bash
docker images
```

执行该命令后，终端会显示出所有本地存储的 Docker 镜像的信息，包括以下内容：

- **REPOSITORY**：镜像的名称或仓库名。
- **TAG**：镜像的标签，通常用于区分不同版本。
- **IMAGE ID**：镜像的唯一标识符。
- **CREATED**：镜像创建的时间。
- **SIZE**：镜像的大小。

这个命令对于查看和管理本地的 Docker 镜像非常有用。

### 终端示例:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker images
REPOSITORY                                                              TAG                            IMAGE ID       CREATED         SIZE
my-fastapi-app                                                          latest                         e7acf350afa6   41 hours ago    169MB
registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test   latest                         e7acf350afa6   41 hours ago    169MB
<none>                                                                  <none>                         55e1f853a63e   42 hours ago    169MB
<none>                                                                  <none>                         56d64b2dbe8c   43 hours ago    161MB
<none>                                                                  <none>                         09c25e8576e3   44 hours ago    130MB
<none>                                                                  <none>                         8e1a6b9da7a7   44 hours ago    130MB
python                                                                  3.11-slim                      10f461201cdb   3 weeks ago     130MB
milvusdb/milvus                                                         v2.3.2                         4b6c62c2b5f8   9 months ago    868MB
minio/minio                                                             RELEASE.2023-03-20T20-16-18Z   400c20c8aac0   17 months ago   252MB
quay.io/coreos/etcd                                                     v3.5.5                         673f29d03de9   23 months ago   182MB
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# 
```

在 `docker images` 的输出中显示 `<none>` 作为 `REPOSITORY` 和 `TAG` 的原因通常与以下两种情况之一有关：

1. **无效或未标记的镜像**： 

   - 当你构建一个 Docker 镜像但没有指定 `--tag` 选项时，镜像会创建成功但不会有名称或标签。结果，在 `docker images` 中会显示 `<none>`。

   - 类似地，如果你删除了一个带有特定 `tag` 的镜像标签，但该镜像仍然存在于 Docker 中，没有任何其他标签与之关联，它也会显示为 `<none>`。

2. **中间层镜像（Dangling Images）**：

   - 当你更新或重新构建一个镜像时，旧的镜像层可能不再需要，但还保留在本地，Docker 将这些镜像标记为 `<none>`。

   - 这些通常是“悬空的”镜像，它们不再与任何标签或容器关联。

### 镜像引用分析:

参考上述 `docker images` 信息，假设你想要删除 `my-fastapi-app` 对应的镜像。

删除前，应该先分析下是否有共用镜像( `IMAGE ID` 相同)的情况(即同一个镜像起了多个容器)，例如:

```bash
REPOSITORY                                                              TAG                            IMAGE ID       CREATED         SIZE
my-fastapi-app                                                          latest                         e7acf350afa6   6 days ago      169MB
registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test   latest                         e7acf350afa6   6 days ago      169MB
```

🚨注意，这两行的 `IMAGE ID` 都是 `e7acf350afa6`，说明这两个标签 (`my-fastapi-app:latest` 和 `registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test:latest`) 实际上指向同一个镜像。

### 镜像和标签的关系

- **镜像**: 是由 `IMAGE ID` 唯一标识的，它代表了实际的存储数据和文件系统层。
- **标签**: 是指向某个镜像的别名。一个镜像可以有多个标签，而这些标签都共享同一个 `IMAGE ID`。

当你删除其中一个标签时，例如 `my-fastapi-app:latest`，镜像本身不会被删除，因为它仍然被另一个标签（`registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test:latest`）引用。

### 镜像引用分析结论:

因此，当你看到多个标签拥有相同的 `IMAGE ID` 时，这意味着它们指向的是同一个镜像。你需要删除所有指向这个镜像的标签，镜像才会从本地存储中完全删除。

### 删除镜像:

```bash
docker rmi my-fastapi-app
docker rmi registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test:latest
```

终端显示:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker rmi my-fastapi-app
Untagged: my-fastapi-app:latest
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker rmi registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test:latest
Untagged: registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test:latest
Untagged: registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test@sha256:7a31f8df4eaebebbc4cb2cd1942c702d68976f34ed0883b051936b3df73f39ae
Deleted: sha256:e7acf350afa617f83402f44d45f2a33b3f8687078bf919ed3c4a56996802cdc3
Deleted: sha256:4d3dbcee5dccadf2c560ca56ee3f7ded8d767ec5495c6eab3b2ac8d5047e9f13
Deleted: sha256:4fd569c4b1b050fb8112857f47e413d0bb48ea1004d1681d955cb1233c295690
Deleted: sha256:91ae11f9e1bcd96165a2eacf44515feeaf3549d32385c92b5bfd01e8c3d683b3
Deleted: sha256:8132666f84f834b626f9deaaa983d3dc25f184c7ec34e95b0b6e1048d8a68fe7
Deleted: sha256:7e20b64410e655f94a1050cb7248c3bb509032aac41075a9f110f450141f1c6f
Deleted: sha256:03da3981c191035438edf16d3d126688353a3817dfd05ee0e2256b3f0e6045d0
Deleted: sha256:5a83e857e8a5539b1fb863785e13ad4b17358d70dc6bd4e63a25aabb03c5eff6
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# 
```

这个输出表示你成功地移除了 `my-fastapi-app:latest` 标签。

这个输出表示你成功地移除了两个特定的Docker镜像( `my-fastapi-app:latest` 和 `registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test:latest` )。在删除后，其对应的文件和存储层也都被清理掉了。

### 如何清理这些 `<none>` 镜像

你可以使用以下命令来删除这些无用的悬空镜像：

```bash
docker image prune
```

这个命令会删除所有没有关联到任何标签的悬空镜像。例如:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker image prune
WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
Deleted Images:
deleted: sha256:09c25e8576e34440623b7b8174664af0e480b95f91c4f3c0355eafc2de80ba39
deleted: sha256:3d9be9055574ef0477855b5023f45ee2eea4ea38afa428b508026bda70060bdd
deleted: sha256:56d64b2dbe8c590d59118a7f4a99b9595a8f6f9930f2c579e6b937aa32f4eaaf
deleted: sha256:e9b86d63587468d963c24f38e4561b90e45fdba5c41752c1d26156c84bf669bd
deleted: sha256:316a614f843d8a421407264c7a72e500e3780566f568ec85bcb939e89dcbc020
deleted: sha256:40a7e4cb2044208abf31639598e814918db988b0a112a274b4d8b751cdec5c23
deleted: sha256:6a05a464d7c1ed4c433869a1b99172bf4831504428e76b18d72ac7776ee62844
deleted: sha256:e47eb39f3630047ac54c7c82555a8d6420fc64dab75f08c028451fc43bb27f8d
deleted: sha256:8e1a6b9da7a74f5e82de334e4264654dfebb9a45096de9bcc2c0518bbeb28971
deleted: sha256:606f6a98d17c8e4ec4c5f19ed32c7333fdfd4020cb5a15cd7c4badbb11351731
deleted: sha256:55e1f853a63e2255a9da99ff0b9e928d67ca6518dcd61c705c639e1e07ca3e67
deleted: sha256:a7b0d53fcfd25ac61288f441759f011110fe47949147b4f3645c148150059a83
deleted: sha256:4d32337ee721058d2fa3c21b910cee886b67fa5a96b8742723303485f5b8b5fc
deleted: sha256:34e013f62e89ca751c6a14ee616c6c22a2bb94c7e3570e814b298ef82a6fa118
deleted: sha256:cb9a11bbe7bdf550abb66c5c280e1ce1c8d799aba360c8ebcd91025385bda01e
deleted: sha256:2da0b4a157e06db892ee3d3e9da5510fbdf1cd3f43d2d0dad1501fae7bd797d4

Total reclaimed space: 70.96MB
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker images
REPOSITORY                                                              TAG                            IMAGE ID       CREATED         SIZE
my-fastapi-app                                                          latest                         e7acf350afa6   42 hours ago    169MB
registry.cn-beijing.aliyuncs.com/peilongchencc_docker_hub/docker_test   latest                         e7acf350afa6   42 hours ago    169MB
python                                                                  3.11-slim                      10f461201cdb   3 weeks ago     130MB
milvusdb/milvus                                                         v2.3.2                         4b6c62c2b5f8   9 months ago    868MB
minio/minio                                                             RELEASE.2023-03-20T20-16-18Z   400c20c8aac0   17 months ago   252MB
quay.io/coreos/etcd                                                     v3.5.5                         673f29d03de9   23 months ago   182MB
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# 
```

### 搜索镜像资源:

```bash
docker search TERM
```

- `TERM`: 你要搜索的关键字或短语，例如镜像的名称或描述。

> [!CAUTION]
> docker search 是专门设计用于从 Docker Hub（即官方的 Docker 镜像仓库）搜索镜像资源的，其他镜像仓库(例如 NGC )上的资源，需要自己去对应网站检索、拉取。

例如:

```bash
docker search pytorch
```

终端效果:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker search pytorch
NAME                                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
pytorch/libtorch-cxx11-builder                                                                    4                    
pytorch/manylinux-cuda113                                                                         0                    
pytorch/manylinux-cuda101                                                                         0                    
bitnami/pytorch                                    Bitnami container image for PyTorch            72                   
pytorch/pytorch-binary-docker-image-ubuntu16.04                                                   6                    
pytorch/manylinux-cuda117                                                                         2                    
pytorch/manylinux-builder                                                                         1                    
pytorch/manylinux-cuda110                                                                         1                    
graphcore/pytorch                                 The Poplar® SDK components required to run P…   4                    
pytorch/torchserve-nightly                        https://github.com/pytorch/serve                3                    
opensciencegrid/osgvo-torch                       OSG VO's Torch base image                       0                    
pytorch/torchaudio_unittest_base                                                                  0                    
pytorch/conda-cuda                                                                                7                    
pytorch/pytorch                                   PyTorch is a deep learning framework that pu…   1096                 
pytorch/manylinux-cuda111                                                                         0                    
intel/intel-optimized-pytorch                     Containers for running PyTorch workloads on …   14                   
intel/intel-extension-for-pytorch                                                                 11                   
airbyte/container-orchestrator                                                                    0                    
pytorch/manylinux-cuda92                                                                          0                    
graphcore/pytorch-jupyter                         The Poplar® SDK plus PyTorch for IPUs includ…   5                    
pytorch/conda-builder                                                                             5                    
nephio/porch-function-runner                                                                      0                    
pytorch/torchserve                                                                                27                   
pytorch/manylinux-cuda102                                                                         4                    
graphcore/pytorch-geometric-jupyter               The Poplar® SDK components required to run P…   2                    
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# 
```