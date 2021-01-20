# CGO

## 带 struct 参数的函数封装

示例：

```go
package main

/*
#include <stdio.h>
#include <stdlib.h>

typedef struct Person {
	int age;
	const char* name;
    void *data;
} Person;

void printPerson(Person p) {
	printf("age = %d\n", p.age);
	printf("name = %s\n", p.name);
	int32_t* d = (int32_t*)(p.data);
	printf("data : %d, %d, %d\n", d[0], d[1], d[2]);
}

*/
import "C"
import "unsafe"

func main() {
	data := []int32{1, 2, 3}

	person := C.Person{
		age:  C.int(100),
		name: C.CString("sheep"),
		data: unsafe.Pointer(&data[0]),
	}

	C.printPerson(person)
}
```

值得注意的是，不同于 c，c++ 中的 int 类型固定 32 位，go 中 int 类型的长度是由机器位数决定的，
因此函数参数中最好使用 int32、int64 等固定长度的类型。
