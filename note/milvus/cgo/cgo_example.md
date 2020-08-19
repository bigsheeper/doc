# cgo

使用 golang 的内置模块 cgo，能够实现 go 对 c/c++ 接口的调用。主要有三种实现方式：go 代码中内嵌 c/c++ 代码、go 直接引用 c/c++ 文件、go 调用 c/c++ 的动/静态库。

无论是哪种实现方式，都需要在 go 文件中导入 cgo 模块：`import "C"`，并在该导入语句的上方插入注释，该注释可以直接是 c/c++ 的代码，也可以是 gcc 的编译选项。

此外，还会介绍指针作为参数在 go 和 c/c++ 中进行交互，以及在使用 go 和 c/c++ 内存中的一些注意事项。

## go 代码中内嵌 c/c++ 代码

在 go 代码中，直接在上述的注释位置内嵌 c 代码，例如：

```go
package main

/*
#include <stdio.h>

void myprint() {
    printf("Hello world\n");
}

*/
import "C"

func main() {
        // test print
        C.myprint()
}
```

但是在实际工程应用中，这种方法显然较为麻烦。

## 在 project 中 go 直接引用 c/c++ 文件

go 中直接引用 c 文件，这种方法结构较为清晰，且可以随时修改查看结果。示例：

示例 project 的目录结构如下：

```txt
cgoExample/
├── main.go
├── test.c
└── test.h
```

test.h

```c
int
sum(int i, int j);
```

test.c

```c
#include "test.h"

int
sum(int i, int j) {
        return i + j + 1;
}
```

main.go

```go
package main

/*
#include "test.c"
*/
import "C"
import "fmt"

func main() {
        // test sum
        fmt.Println(C.sum(1, 10))
}
```

## go 调用 c/c++ 的动态库

go 中指定 gcc 编译选项，指定动态库名称、动态库位置、头文件位置等，从而实现对 c/c++ 库的调用。示例：

示例 project 的目录结构如下：

```txt
cgoExample/
├── lib
│   └── libtest.so
├── main.go
├── test.c
└── test.h
```

test.h 文件与 test.c 文件与 go 直接引用 c/c++ 文件中的示例文件一样。

main.go

```go
package main

/*
#cgo CFLAGS: -I./

#cgo LDFLAGS: -L./lib -ltest -Wl,-rpath=./lib

#include "test.h"
*/
import "C"
import "fmt"

func main() {
        // test sum
        fmt.Println(C.sum(1, 10))
}
```

在 `import "C"` 的上方注释中指定几个参数：

- CFLAGS：指定头文件所在路径，此处即为同级目录 `./`;

- LDFLAGS：-L 用于把新目录添加到库搜索路径上, -l 指定动态库名称 `test`, -Wl,-rpath 指定了运行时搜索动态库的路径

之后，在 lib 目录中使用 gcc 命令编译动态库，生成 libtest.so，main.go 文件便可以脱离 c 源文件运行了：

```bash
gcc -shared -fPIC -o libtest.so ../test.c
```

## 指针参数

可以将指针作为参数传入 c/c++ 接口中进行计算。该指针可以在 go 中进行内存申请（如 make），这种情况下，可以由于 go 的 GC 机制，不要要对内存进行手动管理。此外，指针也可以在 c/c++ 中进行内存申请（如 malloc)，这种情况下就需要手动调用 c 的 free 接口对内存进行释放。

### go 内存指针传入 c/c++

示例项目结构如下：

```txt
cgoPtr/
├── build
│   └── libtest.so
├── main.go
├── test.c
└── test.h
```

test.h

```c
void assign(double ptr[]);
```

test.c

```c
#include <stdlib.h>
#include <stdio.h>

#include "test.h"

void assign(double ptr[]) {
    printf("Hello, c\n");
    int length = 10;

    for (int i = 0; i < length; i++) {
        ptr[i] = i;
        printf("Hello, %d\n", i);
    }
}
```

main.go

```go
package main

/*
#cgo CFLAGS: -I./
#cgo LDFLAGS: -L/home/sheep/go/src/c2go/build -ltest -Wl,-rpath=./build

#include "test.h"
*/
import "C"
import "fmt"

func main() {
        // test ptr
        a := make([]float64, 10)
        C.assign((*C.double)(&a[0]))
        fmt.Println(a[5])
}
```

在该示例中，通过 go 的 make 函数创建一个大小为 10 的 float64 类型的数组，之后将数组强转为 c 的 double 型指针传入 c 函数 assign 中，并在 c 中对数组内的元素进行赋值，且之后不用考虑内存的释放问题。

该示例程序的运行结果如下：

```bash
sheep@sheep:~/go/src/cgoPtr$ go run main.go
Hello, c
Hello, 0
Hello, 1
Hello, 2
Hello, 3
Hello, 4
Hello, 5
Hello, 6
Hello, 7
Hello, 8
Hello, 9
5
```

### go 指针传入 c/c++，在 c/c++ 中分配内存

TODO
