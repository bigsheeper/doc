# Workloads

## Pods

pod 是 kubernetes 中最小的调度单元。一个 pod 中会有一个或多个 container，container 之间会共享存储、网络等资源，此外，pod 中还有关于如何运行 container 的说明。

通常来说，不需要单独创建一个 pod，而是使用 workload 资源进行创建（Deployment、Job 等）。如果需要跟踪 pods 的状态，那么则使用 StatefulSet 进行。

在 kubernetes 集群中，pods 主要有以下作用：

- 只运行一个 container。"one-container-per-Pod"模式是 kubenetes 中最常见的模式，这种情况下，可以认为 pod 是一个 container 的封装，kubernetes 管理 pod 而不是直接操作 container。
- 运行多个需要一起协同工作的 container。

每一个 pod 意味着一个应用程序的示例。如果需要水平扩展应用，那么就应该创建多个 pods，在 kubernetes 中，这叫做 replication。Replicated pods 通常由 workload 资源与其对应的 controlller 来进行管理。

pod 中多个 container 共享资源、互相协作。以下是其中一个使用示例：

![](images/multiple_containers.png)

**Pods and controllers**

Pods 被设计作是一个短暂、用后即弃的实体。当 pod 被创建后，它会被调度至 node 上运行，当 pod 执行结束后就会被驱逐（evicted）。pod 不是一个进程，而是一个运行中的 container 的环境（an environment for running container(s)）。

管理 pods 的 workload 资源有 Deployment、StatefulSet、DaemonSet 等。当一个 node 炸掉时，controller 会检测到该 node 上的 pods 都停止运行了，然后会创建新的 pods，并将它们放置于一个健康的 node 上。

**Pod templates**

示例：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello
spec:
  template:
    # This is the pod template
    spec:
      containers:
      - name: hello
        image: busybox
        command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']
      restartPolicy: OnFailure
    # The pod template ends here
```

Deployment Controller 会保证运行的 pods 与期望状态相符。当 template 更新时，Deployment 会删除已有的 pods 并部署新的 pods。

**Resource sharing and communication**

pod 可以指定一组共享卷，所有在该 pod 中的 container 都可以使用这些卷。

每一个 pod 都会被分配一个独立的 IP 地址，所有在该 pod 中的 container 都共享该 IP 地址。在 pod 内部中，container 可以使用 localhost 互相通信。

**Privileged mode for containers（container 的特权模式）**

可以通过 `privileged` flag 为一个 container 赋予特权，这会使 container 获得操作系统的管理权限。

**Static Pods**

与其他普通 pods 不一样的是，Static pods 由 kubelet daemon 在某个特定节点上进行直接管理而不经过 API server。其主要作用是用于 kubelet 管理 control plane 组件。kubelet 会在 API server 中自动创建一个 static pod 的副本，所以对于 API server 来说，static pod 是只读的。

### Pod Lifecycle

pod 的生命周期: Pending -> Running -> Succeeded/Failed。Pod 在其生命周期中只会被调度一次，一旦其被分配到了一个 node 上后，它就会一直运行直到结束或被终止。

#### Pod lifetime

像 container 中的一个应用程序一样，pod 的寿命是短暂的。Pod 被创建时会被分配一个唯一的 ID（UID），如果一个 node 死掉了，那么其中的 pods 就会被删除。

pod 不会自我修复，如果 node 中的 pod 被调度失败了，那么它就会被删除。

一个 pod 的实例永远不会被重新调度到另一个 node 中，相应的，只会在目标 node 中创建一个新的同名的 pod，但拥有不同的 UID。如果一个 pod 实例被删除了，那么其相应的资源也会被删除。

#### Pod phase

phase 字段位于 `pod.status.phase`。

phase 只是 pod 生命周期的一个简单的高度总结，并不涵盖非常详尽的信息。

![](images/pod_phase.png)

#### Container status

使用命令 `kubectl describe pod <name-of-pod>` 查看 container 信息。

- **waiting**。container 正在为运行做准备，例如正在拉取镜像时。可以使用 kubectl 查看为什么 container 处于 waiting 状态。
- **Running**。container 正在运行。以使用 kubectl 查看 container 何时开始的运行。
- **Terminated**。container 已经结束运行或失败。以使用 kubectl 查看 container 何时开始、何时运行，以及为什么失败。

#### Container restart policy

位于 `pod.spec.restartPolicy` 字段，有 Always、OnFailure、Never 三种，默认为 Always。如果 pod 中的 container 退出了，那么 kubectl 会以幂级数时间（10s，20s，40s...）进行重启。如果重启后的 container 稳定运行超过了 10 min，那么该重启时间将会被重置回 10s。

#### Pod conditions

使用命令 `kubectl describe pod <name-of-pod>` 查看 contition 信息。

- PodScheduled: the Pod has been scheduled to a node.
- ContainersReady: all containers in the Pod are ready.
- Initialized: all init containers have started successfully.
- Ready: the Pod is able to serve requests and should be added to the load balancing pools of all matching Services.

可在 yaml 文件中进行 condition 配置：

![](images/pod_conditions.png)

**Pod readiness**

Pod 是否就绪的一个自定义探针。在 spec.readinessGates 中进行指定，示例：

```yaml
kind: Pod
...
spec:
  readinessGates:
    - conditionType: "www.example.com/feature-1"
status:
  conditions:
    - type: Ready                              # a built in PodCondition
      status: "False"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
    - type: "www.example.com/feature-1"        # an extra PodCondition
      status: "False"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
  containerStatuses:
    - containerID: docker://abcd...
      ready: true
...
```

Pod 只有满足以下两个条件时才会被认为是 Ready 状态：

- Pod 中的所有 container 都已准备就绪。
- conditions 中指定的 readinessGates 为 `True`。

#### Container probes

Probe：kubelet 对 container 进行的周期性诊断。

kubelet 会使用 container 实现的 Handler 进行诊断，hander 类型如下：

- **ExecAction**: Executes a specified command inside the container. The diagnostic is considered successful if the command exits with a status code of 0.
- **TCPSocketAction**: Performs a TCP check against the Pod's IP address on a specified port. The diagnostic is considered successful if the port is open.
- **HTTPGetAction**: Performs an HTTP GET request against the Pod's IP address on a specified port and path. The diagnostic is considered successful if the response has a status code greater than or equal to 200 and less than 400.

每个 Probe 都会返回以下 3 种结果：

- Success: The container passed the diagnostic.
- Failure: The container failed the diagnostic.
- Unknown: The diagnostic failed, so no action should be taken.

kubelet 会在运行的 container 中选择性地执行以下 3 种 Probe：

- **livenessProbe**: Indicates whether the container is running. If the liveness probe fails, the kubelet kills the container, and the container is subjected to its restart policy. If a Container does not provide a liveness probe, the default state is Success.
- **readinessProbe**: Indicates whether the container is ready to respond to requests. If the readiness probe fails, the endpoints controller removes the Pod's IP address from the endpoints of all Services that match the Pod. The default state of readiness before the initial delay is Failure. If a Container does not provide a readiness probe, the default state is Success.
- **startupProbe**: Indicates whether the application within the container is started. All other probes are disabled if a startup probe is provided, until it succeeds. If the startup probe fails, the kubelet kills the container, and the container is subjected to its restart policy. If a Container does not provide a startup probe, the default state is Success.

什么时候需要 liveness probe？如果 container 出现问题那么它就会自己停掉，那就不需要 liveness probe。若 container 未通过 liveness probe，则 container 会被终止或者重启。

什么时候需要 readiness probe？若在 container 就绪后需要给 pod 发送某个请求，则可以使用 readiness probe，也就是会说该请求的发送不会在 container 就绪前发送。若 container 未通过 readiness probe，container 不会被终止或者重启。

什么时候需要 startup probe？若 container 服务持续非常长的时间时，不要使用 liveness probe，而应该使用 startup probe。可以配置一个非常长的时间间隔来进行 startup probe。

#### Termination of Pods

暴力停止应用程序会导致很多资源得不到正确的释放，因此一般来说，当 Container runtime 发送了终止信号后，Container 中的进程终止，API server 才会将相应的 pods 删除。

例子：

1. 使用 kubectl 手动删除某个 pod，默认有 30s 的宽限期。
2. API server 会根据宽限期更新 pod。如果使用 `describe` 命令则可以看到 pods 被标记为了 `Terminating`。之后，kubelet 会看到 pod 被标记为终止了，kubelet 就会开始 pod 的停止进程。如果 container 中定义了 `preStop` hook，那么 kubelet 就会在 Container 中运行该 hook。
3. 在 kubelet 开始 graceful shutdown 的同时，control plane 会移除相应的 pod。ReplicaSets 等资源类型不再将该 pod 视为有效的 replica。
4. 在宽限期内，kubelet 会触发暴力终止。container runtime 会给所有的进程发送 `SIGKILL` 信号。kubelet 还会清除所有暂停的属于该 container runtime 的 container。
5. kubelet 暴力触发 API server 移除相应的 pod。
6. API server 删除 pod 的 API 对象。

grace-period（宽限期）默认为 30s，也可以用过 `--grace-period=<seconds>` 来手动设置宽限期。

设置宽限期为 0，使用命令 `--force --grace-preiod=0` 来进行，在这种情形下，API server 将不再等待 kubelet 中的 pod 终止而是立即删除对应 pod 的 API 对象，在 node 上，pod 还是会有一点点宽限期。

**Garbage collection of failed Pods**

对于失败的 pods，API 对象只会由管理员或 controller 进行删除。当失败的 pods 超过 `terminated-pod-gc-threshold` 时，control plane 会清除这些 pods 以防资源泄露。
