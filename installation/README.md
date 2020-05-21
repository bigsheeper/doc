# arctern/scala

## 1. scala环境搭建

- 安装 Java 8 JDK，见 <https://www.oracle.com/java/technologies/javase-jdk8-downloads.html>

- 安装 sbt
```
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt-get update
sudo apt-get install sbt
```

## 2. 运行
```
cd arctern/scala
sbt
```
等待 build 成功后，在 sbt 交互界面中输入
```
test
```
若要设置 java options, 如增加 GC limit 等，则在运行 test 前在交互界面中输入
```
set javaOptions += "-Xmx5G"
```
