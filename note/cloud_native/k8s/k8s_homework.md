# 6.8 课后作业

1.创建一个 nginx 的 deploy 名称为 nginx-c4 有两个副本

2.更改 1 中创建的 deploy 的副本数为 4,并将镜像改为 daocloud.io/daocloud/dao-2048

3.回滚至两个副本的版本

4.观察在回滚的过程中 deploy annotation 的变化

# anwser

## 1

```bash
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Fri, 24 Jul 2020 10:24:20 +0800
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.14.2
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-6b474476c4 (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  31s   deployment-controller  Scaled up replica set nginx-deployment-6b474476c4 to 2
```

## 2

```bash
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Fri, 24 Jul 2020 10:24:20 +0800
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 2
Selector:               app=nginx
Replicas:               4 desired | 2 updated | 5 total | 3 available | 2 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        daocloud.io/daocloud/dao-2048
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  nginx-deployment-6b474476c4 (3/3 replicas created)
NewReplicaSet:   nginx-deployment-78c685477 (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  71s   deployment-controller  Scaled up replica set nginx-deployment-6b474476c4 to 2
  Normal  ScalingReplicaSet  2s    deployment-controller  Scaled up replica set nginx-deployment-6b474476c4 to 4
  Normal  ScalingReplicaSet  2s    deployment-controller  Scaled up replica set nginx-deployment-78c685477 to 1
  Normal  ScalingReplicaSet  2s    deployment-controller  Scaled down replica set nginx-deployment-6b474476c4 to 3
  Normal  ScalingReplicaSet  2s    deployment-controller  Scaled up replica set nginx-deployment-78c685477 to 2
```

## 3

```bash
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Fri, 24 Jul 2020 10:24:20 +0800
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 3
Selector:               app=nginx
Replicas:               4 desired | 4 updated | 5 total | 3 available | 2 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.14.2
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  nginx-deployment-78c685477 (1/1 replicas created)
NewReplicaSet:   nginx-deployment-6b474476c4 (4/4 replicas created)
Events:
  Type    Reason             Age                 From                   Message
  ----    ------             ----                ----                   -------
  Normal  ScalingReplicaSet  2m13s               deployment-controller  Scaled up replica set nginx-deployment-78c685477 to 1
  Normal  ScalingReplicaSet  2m13s               deployment-controller  Scaled down replica set nginx-deployment-6b474476c4 to 3
  Normal  ScalingReplicaSet  2m13s               deployment-controller  Scaled up replica set nginx-deployment-78c685477 to 2
  Normal  ScalingReplicaSet  2m10s               deployment-controller  Scaled up replica set nginx-deployment-78c685477 to 3
  Normal  ScalingReplicaSet  2m10s               deployment-controller  Scaled down replica set nginx-deployment-6b474476c4 to 1
  Normal  ScalingReplicaSet  2m10s               deployment-controller  Scaled down replica set nginx-deployment-6b474476c4 to 2
  Normal  ScalingReplicaSet  2m10s               deployment-controller  Scaled up replica set nginx-deployment-78c685477 to 4
  Normal  ScalingReplicaSet  4s (x2 over 3m22s)  deployment-controller  Scaled up replica set nginx-deployment-6b474476c4 to 2
  Normal  ScalingReplicaSet  1s (x2 over 2m13s)  deployment-controller  Scaled up replica set nginx-deployment-6b474476c4 to 4
  Normal  ScalingReplicaSet  1s (x6 over 2m7s)   deployment-controller  (combined from similar events): Scaled down replica set nginx-deployment-78c685477 to 1
```
