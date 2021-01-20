# CGO TUTORIAL

## 一、CGO 的使用方式

使用 golang 的内置模块 cgo，能够实现 go 对 c/c++ 接口的调用。主要有三种实现方式：go 代码中内嵌 c/c++ 代码、go 直接引用 c/c++ 文件、go 调用 c/c++ 的动/静态库。

无论是哪种实现方式，都需要在 go 文件中导入 cgo 模块：`import "C"`，并在该导入语句的上方插入注释，该注释可以直接是 c/c++ 的代码，也可以是 gcc 的编译选项。

### go 代码中内嵌 c/c++ 代码

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

### 在 project 中 go 直接引用 c/c++ 文件

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

### go 调用 c/c++ 的动态库

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

## 二、CGO 中的指针

介绍指针作为参数或返回值在 go 和 c/c++ 中进行交互。

在 cgo 中，在 go 中分配了内存的指针叫做 go 指针，在 c/c++ 中分配了内存的指针叫做 c/c++ 指针。

指针在 go 中进行内存申请（如 make），这种情况下，由于 go 的 GC 机制，不需要对内存进行手动管理。

指针在 c/c++ 中进行内存申请（如 malloc)，这种情况下就需要手动调用 c 的 free 接口对内存进行释放。

### go 指针

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

### c/c++ 指针

使用 malloc 函数，在 c/c++ 中分配内存，并在 go 中进行访问，最后，由于该内存不是由 go 进行的管理，所以需要手动对内存进行释放。示例：

示例项目结构如下：

```txt
cgocptr/
├── build
│   └── libtest.so
├── main.go
├── test.c
└── test.h
```

test.h

```c
void* c_malloc(int size);

void cptr_test(void* ptr);

void c_free(void* ptr);
```

test.c

```c
#include <stdlib.h>
#include <stdio.h>

#include "test.h"

#define LENGTH 10

void* c_malloc(int size) {
    void* ptr = malloc(size);
    return ptr;
}

void c_free(void* ptr) {
  if (ptr != NULL) {
    free(ptr);
    ptr = NULL;
  }
}

void cptr_test(void* ptr) {
  for (int i = 0; i < LENGTH; i++) {
    ((double *)ptr)[i] = i;
  }
}
```

main.go

```go
package main

/*
#cgo CFLAGS: -I./

#cgo LDFLAGS: -L/home/sheep/go/src/c2go/build -ltest -Wl,-rpath=./build

#include <stdio.h>
#include <stdlib.h>

#include "test.h"
*/
import "C"
import "fmt"
import "unsafe"
import "reflect"

const length int = 10

func test_c_ptr() {
        var b unsafe.Pointer = C.c_malloc(C.int(8 * length))
        C.cptr_test(b)

        fmt.Println("Pointer type: ", reflect.TypeOf(b))
        if (b == nil) {
                fmt.Println("nullptr error")
                return
        }

        // pointer to array
        b_arr := *(*[length]float64)(b)
        fmt.Println("Array type: ", reflect.TypeOf(b_arr))
        fmt.Println(b_arr)

        C.c_free(b)
}

func main() {
        test_c_ptr()
}
```

在 cgo 中，c 的 void* 与 go 中的 unsafe.Pointer 相对应。在该示例中，首先调用 c_malloc 函数分配一块内存，并返回对应的指针 b，将指针作为参数传入 cptr_test 函数对内存进行赋值。之后将指针转为数组 b_arr 并打印。最后，调用 c_free 函数释放内存。

该示例程序的运行结果如下：

```bash
sheep@sheep:~/go/src/cgocptr$ go run main.go
Pointer type:  unsafe.Pointer
Array type:  [10]float64
[0 1 2 3 4 5 6 7 8 9]
```

## 三、CGO vs C++

在 cgo 中，默认只支持 go 与 c 的交互，因此，若想使用 c++ 的第三方接口或自己编写的 c++ 接口，则需要先使用 c 对 c++ 接口进行封装，再使用 cgo 在 go 中调用。示例：

示例项目结构如下：

```txt
cgoVsCpp/
├── build
│   └── libcwrap.so
├── cwrap.cpp
├── cwrap.h
├── main.go
├── person.cpp
└── person.h
```

person.h

```c++
#pragma once

#include <iostream>

class Person {
public:
    explicit Person(int age);

    int age();

private:
    int age_;
};
```

person.cpp

```c++
#include "person.h"

Person::Person(int age):
  age_(age){}

int Person::age() {
  std::cout << "I'm " << age_ << " years old." << std::endl;
  return age_;
}
```

cwrap.h

```c++
#ifdef __cplusplus
extern "C" {
#endif

typedef void* CPerson;
CPerson PersonInit(int);
int age(CPerson cp);

#ifdef __cplusplus
}
#endif
```

cwrap.cpp

```c++
#include "person.h"
#include "cwrap.h"

CPerson PersonInit(int age) {
  CPerson cp = new Person(age);
  return (void*)cp;
}

int age(CPerson cp) {
  auto p = (Person*)cp;
  return p->age();
}
```

main.go

```go
package main

/*

#cgo CFLAGS: -I./

#cgo LDFLAGS: -L./build -lcwrap -Wl,-rpath=./build

#include "cwrap.h"

*/
import "C"
import "fmt"

func test_person() {
        var person = C.PersonInit(5);
        var age = C.age(person)
        fmt.Println(age)
}

func main() {
        fmt.Println("Test person:")
        test_person()
}
```

在上述示例中，首先在 person.h 中定义了一个 Person 类，并在 person.cpp 中实现其成员函数。然后通过 cwrap.h/cwrap.cpp 文件，通过 C 对 Person 进行封装。

使用如下命令生存动态库 libcwrap.so，则可在 go 文件中对 cwrap 中定义的接口进行调用：

```bash
g++ -shared -fPIC -o libcwrap.so ../person.cpp ../cwrap.cpp
```

## 四、链接静态库

当 c/c++ 的目标库是静态库时，则需要先使用如下命令编译 go：

```bash
go build -ldflags="-extldflags=-static"
```

之后，再运行生成的二进制文件：

```bash
sheep@sheep:~/go/src/sheep_go/cgo/cgoVsCpp$ ./cgoVsCpp 
Test person:
I'm 5 years old.
5
```

## 五、相关资料参考

以上示例代码均可见于 <https://github.com/bigsheeper/sheep_go/tree/master/cgo>

### 参考链接

<https://golang.org/cmd/cgo/>

<https://blog.golang.org/cgo>

<https://stackoverflow.com/questions/1713214/how-to-use-c-in-go/1721230>

<https://github.com/golang/go/tree/master/src/cmd/cgo>

<https://www.marlin.pro/blog/cgo-referencing-c-library-in-go/>

<https://eli.thegreenplace.net/2019/passing-callbacks-and-pointers-to-cgo/>

<https://chai2010.gitbooks.io/advanced-go-programming-book/content/ch2-cgo/ch2-05-internal.html>

<https://www.arp242.net/static-go.html>
