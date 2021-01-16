# golang mutex

## 使用多个函数避免二次上锁

go 里没有重入锁（关于重入锁的概念，请参考java），对一个已经锁上的 mutex 来再次上锁会导致程序死锁。
解决方法：将一个函数分离为多个函数，一个不导出的函数 foo()，这个函数假设锁总是会被保持并去做实际的操作，另一个是导出的函数 Foo()，这个函数会调用 foo()，但在调用前会先去获取锁。
或者使用带有 Foo() 方法的 interface， 在实现了 interface 的类型中实现函数 foo()，因为 foo() 不能被 interface 所调用，因此保证了线程安全。

```go
import "sync"

type Counter interface {
	Add()
}

type CounterImpl struct {
	mu  sync.Mutex
	num int
}

func (c *CounterImpl) add() {
	c.num++
}

func (c *CounterImpl) Add() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.add()
}
```
