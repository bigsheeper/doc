# Homework

## 3.6

### Question

1.安装 docker,并运行一个 nginx

2.给一个容器设置 –cpus –cpuset-cpus 并观察 cpu 的使用

3.一个四核的机器上设置 –cpus=2.5 –cpuset-cpus="0,1" 那么容器最多可以占用多少 cpu 资源?为什么？

### Answer

```bash
sheep@sheep:~/doc$ docker images -a
REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
nginx                           latest              8cf1bfb43ff5        8 days ago          132MB
```

```bash
docker run --cpus=2.5 --cpuset-cpus="0,1" nginx:latest
```

<https://www.cnblogs.com/sparkdev/p/8052522.html>
