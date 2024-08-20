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

```bash
docker build -t my-fastapi-app .
```