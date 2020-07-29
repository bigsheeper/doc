# TiDB Operator

## TiDB 架构

![](tidb_structure.png)

TiDB （计算引擎）
TiKV （存储引擎）
PD   （metadata server 与集群数据调度）

PD 是集群的“大脑”，它一方面是是集群的 metadata server，TiKV 中的数据分布情况都会通过心跳上报给 PD 存储起来；另一方面又承担集群数据调度的任务，我们前面说 TiKV 要把数据拆成更多的 Region 均匀分布到节点上，什么时候拆、怎么拆、拆完分配到哪些节点上这些事情就都是 PD 通过调度算法来决定的。

## TiDB Opetator 架构

```go
// 声明式 API （用户意图的记录） ----> k8s 内置 API CRD ----> TiDBCluster                      \
//     ^                                                      ^                            |
//     |                                                      |                            |
//     |(watch)                                               |(watch)                     |
//     |                                                      |                            |
// 控制循环（控制器） ------------------------------------> tidb-controller-manager           |
//                                                                                         \
//                                                                                         /  TiDB Operator
//                                                                                         |
//                                                       Scheduler Extender(Pod schedule)  |
//                                                                                         |
//                                                                                         |
//                                                                                         |
//                                                       Webhook （验证逻辑，如阻止集群变更）  /
```

典型的 Operator 由 CRD + 控制器组成，PingCap 在此基础上增加了 Scheduler Extender 和 Webhook 构成了 TiDB Operator。

## 实现机制

### 1. 集群构建

TiDB Operator 分别为 PD、TiKV、TiDB 创建一个 StatefulSet，再去管理这些 StatefulSet 来实现优雅升级和故障转移等功能。StatefulSet 提供的语义保证是相同名字的 Pod 集群中同时最多只有一个，StatefulSet 明确定义一组 Pod 中每个的身份，启动和升级都按特定顺序来操作。

### 2. Local PV
