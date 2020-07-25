# Kubebuilder

## 核心概念

### Group、Version、Kinds、Resources

Group：API 功能的集合。

Version: Group 的版本，用于 API 的演进。

Kinds： API GroupVersion 的类型。

Resources： Kind 的对象标识; 在 CRD 中，Kinds 与 Resources 是一对一的。

### Scheme

用于提供 kinds 与 Go types 的映射，每一组 Controller 都需要一个 scheme。

### Informer

主要用于获取 kubernetes 的对象。

### Reconcile

用于实现 Spec 与 Status 的同步。

### Controller

Kubebuidler 为我们生成的脚手架文件，我们只需要实现 Reconcile 方法即可。

### Cache

Kubebuilder 的核心组件，负责在 Controller 进程里面根据 Scheme 同步 Api Server 中所有该 Controller 关心 GVKs 的 GVRs，其核心是 GVK -> Informer 的映射，Informer 会负责监听对应 GVK 的 GVRs 的创建/删除/更新操作，以触发 Controller 的 Reconcile 逻辑。

### Clients

在实现 Controller 的时候不可避免地需要对某些资源类型进行创建/删除/更新，就是通过该 Clients 实现的，其中查询功能实际查询是本地的 Cache，写操作直接访问 Api Server。

### Manager

Kubebuilder 的核心组件，用于：

- 负责运行所有的 Controllers;
- 初始化共享 caches，包含 listAndWatch 功能;
- 初始化 clients 用于与 Api Server 通信。

### Index

由于 Controller 经常要对 Cache 进行查询，Kubebuilder 提供 Index utility 给 Cache 加索引提升查询效率。

### Finalizer

用于告诉 kubernetes GC 删除某个对象。

### OwnerReference

K8s GC 在删除一个对象时，任何 ownerReference 是该对象的对象都会被清除，与此同时，Kubebuidler 支持所有对象的变更都会触发 Owner 对象 controller 的 Reconcile 方法。

## 流程

![](kubebuilder.png)

## API 设计

## 控制器

控制器是 kubernetes 的核心，也是 operator 的核心。控制器用于保证所有的对象的状态与期望的状态想匹配。该过程称为 **reconciling**。

用于保证 reconciling 的所有逻辑都被定义在 **Reconciler** 中。每个 Reconciler 都包含两个元素：期望状态所包含的对象、是否需要重新 reconciling 的 bool 值。

一个控制器与一个 kind 相对应。
