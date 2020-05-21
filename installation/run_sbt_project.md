# 基于 linux terminal 下的 scala 项目搭建与运行

## 1. scala环境搭建

- 安装 Java 8 JDK， <https://www.oracle.com/java/technologies/javase-jdk8-downloads.html>

- 安装 sbt
```
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt-get update
sudo apt-get install sbt
```

## 2. 创建 project
确保 porject 结构如下：
```
- hello-world
    - project (sbt uses this to install and manage plugins and dependencies)
        - build.properties
    - src
        - main
            - scala (All of your scala code goes here)
                - Main.scala (Entry point of program) <-- this is all we need for now
    - build.sbt (sbt's build definition file)
```

## 3. 运行
```
cd project_dir
sbt
```
在 sbt 交互界面中输入
```
run
```