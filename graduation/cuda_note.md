GPU并行计算——指基于CPU+GPU的异构计算架构。
###1.cuda内存结构
CPU+GPU异构计算架构模型如下图所示：![image.png](https://upload-images.jianshu.io/upload_images/14230973-2297f45ba08c1e8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
CPU——host
GPU——device
###2.cuda编程模型
**kernel**，表示在device上线程中并行执行的函数，其函数用`__global__`符号声明，在调用时需要用`<<<grid,block>>>`来指定kernel要执行的线程数量。
此处贴一个不错的视频教学网址：https://www.youtube.com/watch?v=kzXjRFL-gjo
###3.THREAD,BLOCK AND GRID
####thread blocks
![image.png](https://upload-images.jianshu.io/upload_images/14230973-65cc4e14dbb1a9e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####grid
![image.png](https://upload-images.jianshu.io/upload_images/14230973-caa3ae02af1ae839.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####dim 3
![image.png](https://upload-images.jianshu.io/upload_images/14230973-05326b72969e987b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####kernel调用
![image.png](https://upload-images.jianshu.io/upload_images/14230973-83cf320ff7a7e545.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####threadidx
![image.png](https://upload-images.jianshu.io/upload_images/14230973-53b39a55f6bb3ea1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####threadid的计算方式：
`int id = blockidx.x * blockDim.x + threadidx.x`

————————————————————————————————
###4.例子程序
######cpu百万数相加
```
#include <iostream>
#include <math.h>

// function to add the elements of two arrays
void add(int n, float *x, float *y)
{
  for (int i = 0; i < n; i++)
      y[i] = x[i] + y[i];
}

int main(void)
{
  int N = 1<<20; // 1M elements

  float *x = new float[N];
  float *y = new float[N];

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // Run kernel on 1M elements on the CPU
  add(N, x, y);

  // Check for errors (all values should be 3.0f)
  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i]-3.0f));
  std::cout << "Max error: " << maxError << std::endl;

  // Free memory
  delete [] x;
  delete [] y;

  return 0;
}
```







