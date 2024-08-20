# docker内部

本章带大家看一看 docker 容器内部的组成。
- [docker内部](#docker内部)
  - [1. 容器的文件系统](#1-容器的文件系统)
  - [2. 容器的挂载点](#2-容器的挂载点)
  - [3. 容器的日志文件位置](#3-容器的日志文件位置)
  - [4. Docker 数据目录](#4-docker-数据目录)
  - [附录:docker exec指令解释](#附录docker-exec指令解释)
    - [命令结构](#命令结构)
    - [具体参数解释](#具体参数解释)
    - [实际功能](#实际功能)
    - [举例](#举例)
  - [附录: docker exec ... 和 docker inspect ... 的区别](#附录-docker-exec--和-docker-inspect--的区别)


假设你已经构建，并启动了一个docker。例如:

```bash
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                       NAMES
dec75f4de335   my-fastapi-app   "/bin/bash -c '. doc…"   7 minutes ago   Up 7 minutes   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   jolly_cohen
(base) root@iZ2zea5v77oawjy2qz7c20Z:/data/docker_tutorial# 
```

要查找 Docker 容器的数据存储位置，可以从以下几个方面着手：


## 1. 容器的文件系统

Docker 容器的文件系统是基于镜像创建的，并且运行时的所有变化都记录在容器的存储层中。要访问容器的文件系统，可以使用以下命令：

```bash
docker exec -it <CONTAINER_ID> /bin/bash
```

例如，使用你的容器 ID：

```bash
docker exec -it dec75f4de335 /bin/bash
```

> [!TIP]
> 终端输入 `exit` 或 使用快捷键 `Command + D` 可以从 Docker 容器的交互式终端返回到正常模式（即返回到宿主机的命令行界面）。

这会启动一个 bash shell，你可以查看容器内部的文件系统，比如 `/app` 目录，它是你在 `Dockerfile` 中指定的工作目录。例如:

```log
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data# docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
dec75f4de335   my-fastapi-app   "/bin/bash -c '. doc…"   13 minutes ago   Up 13 minutes   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   jolly_cohen
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data# docker exec -it dec75f4de335 /bin/bash
root@dec75f4de335:/app# ll
bash: ll: command not found
root@dec75f4de335:/app# ls
Dockerfile  README.md  __pycache__  dataform  docker_example  docker_example.log  main.py  requirements.txt
root@dec75f4de335:/app# cd dataform/
root@dec75f4de335:/app/dataform# ll
bash: ll: command not found
root@dec75f4de335:/app/dataform# ls
__init__.py  __pycache__  dataform.py
root@dec75f4de335:/app/dataform# cat dataform.py 
from pydantic import BaseModel

# 数据模型
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
root@dec75f4de335:/app/dataform# pwd
/app/dataform
root@dec75f4de335:/app/dataform# exit
exit
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data#
```

⚠️注意: `bash` 环境中没有 `ll` 命令，这是因为它通常是 `ls -l` 的别名，而这种别名在一些基础镜像中未配置。所以你可以直接使用 `ls -l` 来显示文件的详细信息。


## 2. 容器的挂载点

每个 Docker 容器都有一个挂载点，存储了该容器的文件系统。要查看挂载点，可以使用以下命令：

```bash
docker inspect --format='{{.GraphDriver.Data.MergedDir}}' <CONTAINER_ID>
```

例如：

```bash
docker inspect --format='{{.GraphDriver.Data.MergedDir}}' dec75f4de335
```

这将输出容器的实际文件系统位置，例如:

```log
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data# docker inspect --format='{{.GraphDriver.Data.MergedDir}}' dec75f4de335
/var/lib/docker/overlay2/a46222e116fa7ca97e6d34c0c192250df7589575a9c16ce0d119d2be17b77e81/merged
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data# 
```

我们查看下其内部的内容:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/overlay2/a46222e116fa7ca97e6d34c0c192250df7589575a9c16ce0d119d2be17b77e81/merged# ll
total 80
drwxr-xr-x 1 root root 4096 Aug 19 17:36 ./
drwx--x--- 5 root root 4096 Aug 19 17:36 ../
drwxr-xr-x 1 root root 4096 Aug 19 17:36 app/
lrwxrwxrwx 1 root root    7 Aug 12 08:00 bin -> usr/bin/
drwxr-xr-x 2 root root 4096 Mar 30 01:20 boot/
drwxr-xr-x 1 root root 4096 Aug 19 17:36 dev/
-rwxr-xr-x 1 root root    0 Aug 19 17:36 .dockerenv*
drwxr-xr-x 1 root root 4096 Aug 19 17:36 etc/
drwxr-xr-x 2 root root 4096 Mar 30 01:20 home/
lrwxrwxrwx 1 root root    7 Aug 12 08:00 lib -> usr/lib/
lrwxrwxrwx 1 root root    9 Aug 12 08:00 lib64 -> usr/lib64/
drwxr-xr-x 2 root root 4096 Aug 12 08:00 media/
drwxr-xr-x 2 root root 4096 Aug 12 08:00 mnt/
drwxr-xr-x 2 root root 4096 Aug 12 08:00 opt/
drwxr-xr-x 2 root root 4096 Mar 30 01:20 proc/
drwx------ 1 root root 4096 Aug 19 17:52 root/
drwxr-xr-x 3 root root 4096 Aug 12 08:00 run/
lrwxrwxrwx 1 root root    8 Aug 12 08:00 sbin -> usr/sbin/
drwxr-xr-x 2 root root 4096 Aug 12 08:00 srv/
drwxr-xr-x 2 root root 4096 Mar 30 01:20 sys/
drwxrwxrwt 1 root root 4096 Aug 19 16:49 tmp/
drwxr-xr-x 1 root root 4096 Aug 12 08:00 usr/
drwxr-xr-x 1 root root 4096 Aug 12 08:00 var/
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/overlay2/a46222e116fa7ca97e6d34c0c192250df7589575a9c16ce0d119d2be17b77e81/merged# cd app
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/overlay2/a46222e116fa7ca97e6d34c0c192250df7589575a9c16ce0d119d2be17b77e81/merged/app# ll
total 44
drwxr-xr-x 1 root root 4096 Aug 19 17:36 ./
drwxr-xr-x 1 root root 4096 Aug 19 17:36 ../
drwxr-xr-x 1 root root 4096 Aug 19 17:36 dataform/
drwxr-xr-x 5 root root 4096 Aug 19 16:49 docker_example/
-rw-r--r-- 1 root root  206 Aug 20 02:08 docker_example.log
-rw-r--r-- 1 root root 1742 Aug 19 16:35 Dockerfile
-rw-r--r-- 1 root root 1232 Aug 19 16:06 main.py
drwxr-xr-x 2 root root 4096 Aug 19 17:36 __pycache__/
-rw-r--r-- 1 root root 2003 Aug 19 14:01 README.md
-rw-r--r-- 1 root root   22 Aug 19 10:40 requirements.txt
```

🚀发现了吗？如果只以文件内容判断，`docker inspect --format='{{.GraphDriver.Data.MergedDir}}' dec75f4de335` 和 `docker exec -it dec75f4de335 /bin/bash` 显示的结果是一样的。

🚨注意: 

你在 `docker inspect` 的路径下看到的文件和目录，不仅仅是你应用程序的 `app` 目录，而是整个容器的文件系统视图。

这是因为 Docker 容器的文件系统模拟了一个完整的操作系统环境，以便应用程序可以在其中运行。


## 3. 容器的日志文件位置

容器的日志文件默认存储在 Docker 的日志目录中（通常是 `/var/lib/docker/containers/`）。要查看某个容器的日志，可以使用以下命令：

```bash
docker logs <CONTAINER_ID>
```

例如：

```bash
docker logs dec75f4de335
```

终端显示:

```log
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data# docker logs dec75f4de335
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8848 (Press CTRL+C to quit)
INFO:     172.17.0.1:35786 - "GET /items/1?q=test HTTP/1.1" 200 OK
INFO:     172.17.0.1:56454 - "GET / HTTP/1.1" 200 OK
(langchain) root@iZ2zea5v77oawjy2qz7c20Z:/data#
```

我前面说了，日志存储在 `/var/lib/docker/containers/` 路径，我们进入其中看一下:

```log
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/containers/dec75f4de335183a9323cd1d91e5167d33249ef0400d182c6bbf54eefa8dfbf2# ll
total 44
drwx--x--- 4 root root 4096 Aug 19 17:36 ./
drwx--x--- 6 root root 4096 Aug 19 17:37 ../
drwx------ 2 root root 4096 Aug 19 17:36 checkpoints/
-rw------- 1 root root 3318 Aug 19 17:36 config.v2.json
-rw-r----- 1 root root  976 Aug 20 03:43 dec75f4de335183a9323cd1d91e5167d33249ef0400d182c6bbf54eefa8dfbf2-json.log
-rw------- 1 root root 1476 Aug 19 17:36 hostconfig.json
-rw-r--r-- 1 root root   13 Aug 19 17:36 hostname
-rw-r--r-- 1 root root  174 Aug 19 17:36 hosts
drwx--x--- 2 root root 4096 Aug 19 17:36 mounts/
-rw-r--r-- 1 root root  813 Aug 19 17:36 resolv.conf
-rw-r--r-- 1 root root   71 Aug 19 17:36 resolv.conf.hash
(base) root@iZ2zea5v77oawjy2qz7c20Z:/var/lib/docker/containers/dec75f4de335183a9323cd1d91e5167d33249ef0400d182c6bbf54eefa8dfbf2# cat dec75f4de335183a9323cd1d91e5167d33249ef0400d182c6bbf54eefa8dfbf2-json.log 
{"log":"INFO:     Started server process [1]\n","stream":"stderr","time":"2024-08-19T09:36:16.972328944Z"}
{"log":"INFO:     Waiting for application startup.\n","stream":"stderr","time":"2024-08-19T09:36:16.972365651Z"}
{"log":"INFO:     Application startup complete.\n","stream":"stderr","time":"2024-08-19T09:36:16.972500983Z"}
{"log":"INFO:     Uvicorn running on http://0.0.0.0:8848 (Press CTRL+C to quit)\n","stream":"stderr","time":"2024-08-19T09:36:16.972777094Z"}
{"log":"INFO:     172.17.0.1:35786 - \"GET /items/1?q=test HTTP/1.1\" 200 OK\n","stream":"stdout","time":"2024-08-19T09:53:23.418318226Z"}
{"log":"INFO:     172.17.0.1:56454 - \"GET / HTTP/1.1\" 200 OK\n","stream":"stdout","time":"2024-08-19T09:53:56.654166154Z"}
{"log":"INFO:     147.185.133.203:65450 - \"GET / HTTP/1.1\" 200 OK\n","stream":"stdout","time":"2024-08-19T18:08:35.317008182Z"}
{"log":"WARNING:  Invalid HTTP request received.\n","stream":"stderr","time":"2024-08-19T19:43:04.49951909Z"}
```

> [!NOTE]
> `*-json.log` 文件以 JSON 格式存储了原始日志数据，`docker logs` 会对日志内容进行格式化。


## 4. Docker 数据目录

Docker 的所有容器、镜像、卷、网络等数据默认存储在 `/var/lib/docker` 目录下。如果你没有指定数据目录的其他位置（通过修改 Docker 配置），则这个目录是容器文件系统和其他数据的存储位置。

通过这些方法，你可以查看容器的文件、日志以及在宿主机上的存储路径。


## 附录:docker exec指令解释

```bash
docker exec -it dec75f4de335 /bin/bash
```

这条指令用于在 Docker 容器中启动一个 **交互式终端会话** 。以下是对该命令的详细解释：

### 命令结构

```bash
docker exec -it <container_id> <command>
```

### 具体参数解释

- **docker exec**: `docker exec` 命令用于在已经运行的容器中执行命令。这与 `docker run` 不同，后者是创建并运行一个新的容器。
  
- **-it**: 这是两个选项的组合：
  - **-i**: 让容器保持标准输入（STDIN）打开。这样可以进行交互式输入(默认情况下，你不能与容器内运行的进程进行交互输入)。
  - **-t**: 分配一个伪终端（TTY）。这使得你可以在容器中获得一个命令行界面。
  
- **dec75f4de335**: 这是容器的 ID，可以是容器的全名或部分 ID。这个 ID 标识了你要进入的目标容器。

- **/bin/bash**: 这是要在容器中执行的命令。在这里，它启动了一个 Bash shell，使你能够在容器内运行命令。

### 实际功能

这条命令会让你进入名为 `dec75f4de335` 的 Docker 容器，并在其中启动一个交互式的 Bash shell。你可以像在普通 Linux 服务器上一样，在这个终端内执行各种命令。

### 举例

假设你有一个运行中的容器，并且你想查看或调试该容器的内部环境，那么你可以运行这条命令来进入该容器，然后执行例如 `ls`、`cat` 等操作。

例如，运行该命令后，你可能看到如下的提示符：

```bash
root@dec75f4de335:/app#
```

这表明你已经成功进入了容器的命令行环境。


## 附录: docker exec ... 和 docker inspect ... 的区别

使用 `docker exec -it dec75f4de335 /bin/bash` 和通过 `docker inspect --format='{{.GraphDriver.Data.MergedDir}}' dec75f4de335` 查看到的结果虽然相同，但在目的和使用方式上有所不同。以下是二者的区别：

1. `docker exec -it dec75f4de335 /bin/bash`

   - 功能: 通过这个命令，你可以进入一个正在运行的容器内部，并在其中启动一个交互式的 shell（例如 `/bin/bash`）。

   - 使用场景: 当你希望以容器的视角查看或操作文件系统时，可以使用这个命令。这相当于进入了容器内部，你看到的是容器的文件系统视图。例如，执行 `ls` 命令会列出容器内的文件和目录。

   - 结果: 你看到的文件和目录是在容器环境中的。文件路径和权限等信息都是基于容器内的视角，与宿主机隔离。

2. `docker inspect --format='{{.GraphDriver.Data.MergedDir}}' dec75f4de335`

   - 功能: 这个命令直接在宿主机上查找并显示该容器的文件系统在宿主机上的物理存储位置（目录路径）。它不进入容器，而是从宿主机的角度查看文件系统。

   - 使用场景: 当你需要从宿主机直接访问或查看容器文件系统，或进行低级别调试（例如文件权限问题）时，使用这个命令。你可以在宿主机的命令行中直接访问这个路径。

   - 结果: 你看到的是容器文件系统在宿主机上的存储位置，可以直接在宿主机上查看、编辑容器内的文件。这是容器文件系统在宿主机上的真实路径。

主要区别:

- 视角不同: `docker exec` 是从容器的视角看文件系统，而 `docker inspect` 是从宿主机的视角看容器的文件系统。

- 权限与隔离: 在 `docker exec` 中，你操作的环境是容器内的，受容器权限和隔离的限制。而在 `docker inspect` 中，你是以宿主机的权限直接访问容器文件系统，突破了容器的隔离性。

简言之，`docker exec` 是在容器内部工作，而 `docker inspect` 是在宿主机外部、直接查看容器在宿主机上的物理存在。