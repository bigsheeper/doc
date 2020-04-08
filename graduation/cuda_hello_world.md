成功运行hello world cuda程序，代码如下：

```
    #include "cuda_runtime.h"

    #include <stdio.h>

    __global__ void helloFromGPU(void)

    {

    printf("Hello World from GPU!\n");

    }

    int main() {

    helloFromGPU<<<1,1>>>();

    cudaDeviceReset();

    getchar();

    return 0;

    }
```

查看GPU配置属性
```
    #include "cuda_runtime.h"

    #include <cuda.h>

    #include <stdio.h>

    #include <stdlib.h>

    #include <iostream>

    using namespace std;

    __global__ void helloFromGPU(void)

    {

    printf("Hello World from GPU!\n");

    }

    int main() {

    helloFromGPU<<<1,1>>>();

    cudaDeviceReset();

    int dev = 0;

    cudaDeviceProp devProp;

    cudaGetDeviceProperties(&devProp, dev);

    cout << "Use GPU device " << dev << ": " << devProp.name << endl;

    cout << "The num of SM:" << devProp.multiProcessorCount << endl;

    cout << "Shared menory per block:" << devProp.sharedMemPerBlock / 1024.0 << " KB" << endl;

    cout << "Max threads per block:" << devProp.maxThreadsPerBlock << endl;

    cout << "Max threads per multiprocessor:" << devProp.maxThreadsPerMultiProcessor << endl;

    cout << "Max threads per EM:" << devProp.maxThreadsPerMultiProcessor / 32 << endl;

    getchar();

    return 0;

    }
```