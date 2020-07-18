# Install And Run Go

## 配置环境

### 1. 下载

```bash
wget https://golang.org/dl/go1.14.6.linux-amd64.tar.gz
```

### 2. 解压并配置

```bash
tar -zxf go1.14.6.linux-amd64.tar.gz
export GOROOT=/PATH_TO/go
export GOPATH=$HOME/go
export PATH=$PATH:/PATH_TO/go/bin
```

## 运行 hello world

创建 hello.go 文件：

```go
package main

import "fmt"

func main() {
   fmt.Println("Hello, World!")
}
```

运行：

```bash
go run hello.go
```

## 运行 Project

在 Project 主目录中下载所有的依赖：

```bash
go get ./...
```

之后以同样的方式运行 Project 中带有 main 函数的测试文件：

```bash
go run test.go
```
