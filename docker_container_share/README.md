# 介绍将docker容器分享给他人

本章介绍如何将自己的docker容器分享给他人。
- [介绍将docker容器分享给他人](#介绍将docker容器分享给他人)
  - [前提条件:](#前提条件)
  - [方法 1:将镜像保存为 tar 文件](#方法-1将镜像保存为-tar-文件)
    - [1. 将容器打包成镜像(可选)](#1-将容器打包成镜像可选)
    - [2. 将镜像保存为 tar 文件](#2-将镜像保存为-tar-文件)
    - [3. 分享 tar 文件](#3-分享-tar-文件)
    - [4. 对方加载镜像并启动容器](#4-对方加载镜像并启动容器)
  - [方法 2:将镜像推送到 Docker Registry](#方法-2将镜像推送到-docker-registry)


## 前提条件:

假设你已经将你的应用程序打包成了一个docker，效果如下:

```bash
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED        STATUS        PORTS                                       NAMES
dec75f4de335   my-fastapi-app   "/bin/bash -c '. doc…"   17 hours ago   Up 17 hours   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   jolly_cohen
```

通常有两种方法将Docker镜像分享给他人:


## 方法 1:将镜像保存为 tar 文件

### 1. 将容器打包成镜像(可选)

> [!NOTE]
> 如果你在容器运行后，没有对其进行更改，可以跳过这一节，直接使用 `docker save` 指令。

如果你在容器运行后对其进行了更改（比如安装软件、修改配置），这些更改不会自动反映在原始镜像中。因此，你需要使用 `docker commit` 将这些更改保存为一个新的镜像。可以参考下列指令:

```bash
docker commit <CONTAINER_ID> <your_image_name>
```

例如:

```bash
docker commit dec75f4de335 my-fastapi-app:latest
```

### 2. 将镜像保存为 tar 文件

使用 `docker save` 命令将镜像保存为一个 tar 文件:

```bash
docker save -o <path_to_output_tar_file> <your_image_name>
```

例如:

```bash
docker save -o my-fastapi-app.tar my-fastapi-app:latest
```

🚨注意:

`my-fastapi-app:latest` 对应的是 `docker ps` 显示的 `IMAGE`。如果你看过笔者写的[simple_example](../simple_example/README.md)章节，应该就理解对应关系了。

### 3. 分享 tar 文件

你可以通过任何文件传输方式（如网络分享、U盘等）将这个 tar 文件分享给其他人。如果你采用`scp`传输给他人的服务器，可以参考下列写法:

```bash
scp -P 13120 /Users/peilongchencc/Downloads/my-fastapi-app.tar root@js1.blockelite.cn:/root/data/
root@js1.blockelite.cn's password:
my-fastapi-app.tar                            100%  168MB   1.6MB/s   01:44
```

### 4. 对方加载镜像并启动容器

收到 tar 文件后，对方可以使用 `docker load` 加载镜像:

```bash
docker load -i <path_to_tar_file>
```

然后通过以下命令运行容器:

```bash
docker run -d -p 8848:8848 <your_image_name>
```

例如，笔者将`tar`文件传给另一台服务器后。终端运行下列指令加载镜像:

```bash
docker load -i my-fastapi-app.tar
```

终端显示:

```log
(base) root@ubuntu22:~/data# docker load -i my-fastapi-app.tar
9853575bc4f9: Loading layer [==================================================>]  77.83MB/77.83MB
c897e8952453: Loading layer [==================================================>]  9.539MB/9.539MB
29fa0c9cc49b: Loading layer [==================================================>]  35.32MB/35.32MB
fdf783cf2812: Loading layer [==================================================>]  4.608kB/4.608kB
3db20f592cb9: Loading layer [==================================================>]  12.28MB/12.28MB
272f89564662: Loading layer [==================================================>]  1.536kB/1.536kB
962fb116696f: Loading layer [==================================================>]  12.29kB/12.29kB
3c76de850261: Loading layer [==================================================>]  41.42MB/41.42MB
Loaded image: my-fastapi-app:latest
(base) root@ubuntu22:~/data#
```

终端运行下列指令启动容器:

```bash
docker run -d -p 8848:8848 my-fastapi-app:latest
```

终端显示:

```log
(base) root@ubuntu22:~/data# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(base) root@ubuntu22:~/data# docker run -d -p 8848:8848 my-fastapi-app:latest
e81f4c27bd5670450ac7c677544292a9f4b5f8d55903c290c0cfd9a710545477
(base) root@ubuntu22:~/data# docker ps
CONTAINER ID   IMAGE                   COMMAND                   CREATED          STATUS          PORTS                                       NAMES
e81f4c27bd56   my-fastapi-app:latest   "/bin/bash -c '. doc…"   16 seconds ago   Up 14 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   quizzical_snyder
(base) root@ubuntu22:~/data# 
```


## 方法 2:将镜像推送到 Docker Registry

这种方式适合共享给多个用户，或者你不希望使用文件传输。

1. 将镜像推送到 Docker Hub（或其他 Registry）
   你需要先登录 Docker Hub:
   ```bash
   docker login
   ```
   然后为镜像打标签并推送到 Docker Hub:
   ```bash
   docker tag <your_image_name> <your_dockerhub_username>/<your_image_name>:latest
   docker push <your_dockerhub_username>/<your_image_name>:latest
   ```
   例如:
   ```bash
   docker tag my-fastapi-app mydockerhubuser/my-fastapi-app:latest
   docker push mydockerhubuser/my-fastapi-app:latest
   ```

2. 让其他人从 Docker Hub 拉取镜像
   其他人可以通过以下命令从 Docker Hub 拉取镜像并运行容器:
   ```bash
   docker pull <your_dockerhub_username>/<your_image_name>:latest
   docker run -d -p 8848:8848 <your_dockerhub_username>/<your_image_name>:latest
   ```

这两种方法都可以让其他人获取并运行你打包好的 Docker 容器。根据你的实际需求选择合适的方式即可。