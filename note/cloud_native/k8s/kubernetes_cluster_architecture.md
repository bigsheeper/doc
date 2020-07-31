# Cluster Architecture

## Nodes

node 可以在一个物理机上，也可以在一个虚拟机上。node 由 control plane 来控制。

### management

给 API server 中添加 nodes 的两种方式：

- kubelet 向 control plane 中注册。
- 管理员手动添加 node 对象。

### Self-registration of Nodes

当 kubelet 中的 `--register-node` flag 为 true （默认也为 true）时，kubelet 会自动向 API server 进行注册。

一些参数：

- --kubeconfig - 用于向 apiserver 表明身份的凭据路径。
- --cloud-provider - 如何从云服务商读取关于自己的元数据。
- --register-node - 自动向 API 服务注册。
- --register-with-taints - 使用 tains 列表注册节点。
- --node-ip - 节点 IP 地址。
- --node-labels - 在集群中注册节点时要添加的标签。
- --node-status-update-frequency - 指定 kubelet 向控制面组件发送状态的频率。

### Manual Node administration

可以通过 kubectl 创建或修改 node 对象。

### Node Status

使用 `kubectl describe node <insert-node-name-here>` 来查看 node 状态。

#### 1. Addresses

HostName：由节点的内核设置。可以通过 kubelet 的 --hostname-override 参数覆盖。
ExternalIP：通常是节点的可以外部路由（从集群外可访问）的 IP 地址。
InternalIP：通常是节点的仅可在集群内部路由的 IP 地址

#### 2. Conditions

用于描述所有正在运行的 nodes 的状态。

![](images/node_contition.png)

#### 3. Capacity and Allocatable

描述节点上的可用资源：CPU、内存和 Pods 的个数上限。
capacity 中的字段指示节点拥有的资源总量。allocatable 指示节点上可供普通 Pod 消耗的资源量。

#### 4. Info

OS name、kernel version、kubernetes version 等等。

#### 示例

```bash
sheep@sheep:~/doc/note/cloud_native/k8s/yaml$ kubectl get node
NAME       STATUS   ROLES    AGE   VERSION
minikube   Ready    master   7d    v1.18.3
sheep@sheep:~/doc/note/cloud_native/k8s/yaml$ kubectl describe node minikube
Name:               minikube
Roles:              master
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=minikube
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=5664228288552de9f3a446ea4f51c6f29bbdd0e0-dirty
                    minikube.k8s.io/name=minikube
                    minikube.k8s.io/updated_at=2020_07_23T16_24_43_0700
                    minikube.k8s.io/version=v1.12.1
                    node-role.kubernetes.io/master=
Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: /var/run/dockershim.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Thu, 23 Jul 2020 16:24:39 +0800
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  minikube
  AcquireTime:     <unset>
  RenewTime:       Thu, 30 Jul 2020 17:02:25 +0800
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  MemoryPressure   False   Thu, 30 Jul 2020 16:59:31 +0800   Thu, 23 Jul 2020 16:24:35 +0800   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure     False   Thu, 30 Jul 2020 16:59:31 +0800   Thu, 23 Jul 2020 16:24:35 +0800   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure      False   Thu, 30 Jul 2020 16:59:31 +0800   Thu, 23 Jul 2020 16:24:35 +0800   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready            True    Thu, 30 Jul 2020 16:59:31 +0800   Thu, 23 Jul 2020 16:25:01 +0800   KubeletReady                 kubelet is posting ready status
Addresses:
  InternalIP:  172.17.0.2
  Hostname:    minikube
Capacity:
  cpu:                12
  ephemeral-storage:  245016792Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             32853544Ki
  pods:               110
Allocatable:
  cpu:                12
  ephemeral-storage:  245016792Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             32853544Ki
  pods:               110
System Info:
  Machine ID:                 aeb18d9e0d6846f1a083b25386303de7
  System UUID:                18bfc12f-01f8-4398-963c-669cb9964457
  Boot ID:                    9b069bed-e46d-4545-bb4a-f01015f8ec29
  Kernel Version:             4.15.0-112-generic
  OS Image:                   Ubuntu 19.10
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  docker://19.3.2
  Kubelet Version:            v1.18.3
  Kube-Proxy Version:         v1.18.3
Non-terminated Pods:          (13 in total)
  Namespace                   Name                                 CPU Requests  CPU Limits  Memory Requests  Memory Limits  AGE
  ---------                   ----                                 ------------  ----------  ---------------  -------------  ---
  default                     annotations-demo                     0 (0%)        0 (0%)      0 (0%)           0 (0%)         4h48m
  default                     nginx-demo                           0 (0%)        0 (0%)      0 (0%)           0 (0%)         6h31m
  default                     nginx-deployment-6b474476c4-4mvmv    0 (0%)        0 (0%)      0 (0%)           0 (0%)         6h50m
  default                     nginx-deployment-6b474476c4-ck6tn    0 (0%)        0 (0%)      0 (0%)           0 (0%)         6h50m
  default                     nginx-f89759699-8z8lq                0 (0%)        0 (0%)      0 (0%)           0 (0%)         6h51m
  kube-system                 coredns-546565776c-tfj8p             100m (0%)     0 (0%)      70Mi (0%)        170Mi (0%)     7d
  kube-system                 etcd-minikube                        0 (0%)        0 (0%)      0 (0%)           0 (0%)         7d
  kube-system                 kube-apiserver-minikube              250m (2%)     0 (0%)      0 (0%)           0 (0%)         7d
  kube-system                 kube-controller-manager-minikube     200m (1%)     0 (0%)      0 (0%)           0 (0%)         7d
  kube-system                 kube-proxy-xw4x4                     0 (0%)        0 (0%)      0 (0%)           0 (0%)         7d
  kube-system                 kube-scheduler-minikube              100m (0%)     0 (0%)      0 (0%)           0 (0%)         7d
  kube-system                 storage-provisioner                  0 (0%)        0 (0%)      0 (0%)           0 (0%)         7d
  kube-system                 tiller-deploy-fc55974f-8vwg5         0 (0%)        0 (0%)      0 (0%)           0 (0%)         6d
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests   Limits
  --------           --------   ------
  cpu                650m (5%)  0 (0%)
  memory             70Mi (0%)  170Mi (0%)
  ephemeral-storage  0 (0%)     0 (0%)
  hugepages-1Gi      0 (0%)     0 (0%)
  hugepages-2Mi      0 (0%)     0 (0%)
Events:              <none>
```

### Node controller

node controller 是 control plane 的其中一个组件，用来管理 nodes 的方方面面。

在 node 的生命周期中，node controller 主要负责以下几个工作：

- 分配 CIDR。
- 保持节点控制器内部的节点列表与云服务商所提供的可用机器列表同步。
- 监测 node 的健康。

### Heartbeats

由 nodes 发起，用来表示当前 node 是否可用。

heartbeats 有两种：

- NodeStatus。当 node 状态发生变化时，kubelet 会更新 NodeStatus。即使 node 状态没有发生变化， kubelet 也会默认每 5 分钟更新一次 NodeStatus。
- Lease 对象。每个 node 都有一个 Lease 对象，位于 kube-node-lease namespace 中。当 node 状态发生变化时，kubelet 会更新 Lease。即使 node 状态没有发生变化， kubelet 也会默认每 10 秒钟更新一次 Lease。

### Reliability

大部分情况下，Node controller 把驱逐速率限制在 `--node-eviction-rate` 个（默认为 0.1）每秒。表示每 10 秒内最多驱逐一个节点。此外驱逐策略还会因为集群规模而变化。详细见：<https://kubernetes.io/docs/concepts/architecture/nodes/#reliability>。

### Node Capacity

node 对象会自动追踪 node 中资源的 capacity 信息（例如，内存、CPU 数等）。当 node 是手动创建时，那么该 capacity 信息就要由创建者来手动设置了。

## Control Plane-Node Communication

### Node to Control Plane

<https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/#node-to-control-plane>

### Control Plane to Node

<https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/#control-plane-to-node>

## Controllers

control loop 是用于管理系统状态的一个 non-terminating loop。controller 观测着集群，让集群的状态始终从 current state 向 desired state 靠拢。

### Controller 模式

#### 通过 API server 进行控制

kubernetes 的内置 controller 都是通过与 API server 进行交互来实现的。Job Controller 就是其中一个。当 Job Controller 检测到一个新的任务时，它会保证有正确运行的 Pod 数量。Controller 内部不会运行任何 pods 或 containers，它只会负责告诉 API server 去创建或移除 pods，而其他的工作会交由 control plane 的其他组件来完成。

#### 直接控制

对于集群外的资源，Controller 会直接与其交互，让系统往 desired state 靠拢。

### Desired state & Current state

由于 Controller 的存在，集群的状态可能会在任意时刻改变，也就是说集群的状态是不稳定的。

### 设计思路

通常来说，kubernetes 会有一个 controller 来保证一个资源类型（kind）达到期望状态，同时还会有另一个 kind 的 controller 来进行管理以确保期望状态会发生。

可能会有多个 controller 来创建同一种 kind 对象。但 controller 只会管理与其关联的对象。例如，deployment 和 job 都创建的 pods，删除 deployment 时它只会删除它创建的 pods，而不会删除 job 创建的 pods。

## Cloud Controller Manager

<https://kubernetes.io/docs/concepts/architecture/cloud-controller/>
