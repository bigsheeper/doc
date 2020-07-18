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

go 会默认建立一个全局仓库 $HOME/go
之后，在 Project 主目录中导入所有的依赖，依赖将会被导入至 $GOPATH 中：

```bash
go get ./...
```

以同样的方式运行 Project 中带有 main 函数的测试文件：

```bash
go run test.go
```

## 在 IDE goland 中配置运行 Project

### 1. 使用 goland 打开 Project，

### 2. 设置 GOROOT

在 Settings->Go->GOROOT 中设置 SDK，可选择在线下载或本地导入

### 3. 设置 GOPATH

在 Settings->Go->GOPATH 中将 Global GOPATH 设置为 $HOME/go

