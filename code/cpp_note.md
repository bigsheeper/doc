####1、右值引用与move
左值——可被引用的数据对象，即可通过地址访问的对象
右值——字面常量、表达式等中间结果，不能获取到地址

左值引用——传统的C++引用，如   int i = 10;   int &refi = i;
右值引用——对右值的引用，用于获取临时变量的存储地址，如int &&i2 = 10;

左值持久，右值短暂;
https://www.jianshu.com/p/31cea1b6ee24
https://www.cnblogs.com/likaiming/p/9045642.html
https://www.jianshu.com/p/b90d1091a4ff
https://www.cnblogs.com/qicosmos/p/4325949.html

####2、参数绑定
https://blog.csdn.net/qq_37653144/article/details/79285221

####3、inline
定义在类中的成员函数都是inline的，如果仅仅只是给出了声明那么它不是inline的，需要在**类外**加上inline关键字
inline必须与函数定义体放在一起

####4、extern
1）在不同文件中分离变量的声明和定义
2）在多个文件中共享const对象
```
//file1.cpp定义并初始化和一个常量，该常量能被其他文件访问
extern const int bufferSize = function();
//file1.h头文件
extern const int bufferSize; //与file1.cpp中定义的是同一个
```
3）模板的控制与实例化
extern template class vec<string>;       //声明
template int sum(const int, const int);  //定义
当编译器遇到extern模板声明时，它不会在本文件中生成实例化代码，将一个实例化声明为extern就表示承诺在程序的其他位置有该实例化的一个非extern定义。对于一个给定的实例化版本，可能有多个extern声明，但必须只有一个定义。
