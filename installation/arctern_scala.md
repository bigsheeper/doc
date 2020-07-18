# arctern/scala

## 1. scala 环境搭建
- 安装 Java 8 JDK，见 <https://www.oracle.com/java/technologies/javase-jdk8-downloads.html>
- 安装 sbt
```
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt-get update
sudo apt-get install sbt
```

## 2. 编译
```
cd arctern/scala
sbt
```
- 可使用 -D 传入编译参数。例如选择 spark 的版本，则使用如下命令编译
```
sbt -DsparkVersion="2.4.5"
```

## 3. 运行
在 sbt 交互界面中输入
```
test
```
- 可使用 set 进行相关设置。例如设置 java GC limit，则在交互界面中输入
```
set javaOptions += "-Xmx5G"
```

