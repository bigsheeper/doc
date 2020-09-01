# Query Node

## 功能

- 接受消息：对接 pulsar client，接收 Message;
- 消息处理：将接受到的 Message 重组为 id、timestamp、dataChunk，调用 milvus core 进行 Insert、Delete、Search 等操作;
- 消息缓冲：提供消息缓冲区，将接受到的待处理消息放入缓冲区中;
- 接口封装：使用 cgo 调用 milvus core 封装的 c 接口;
- 对象管理：封装 Collection、Partition、Segment 对象，对其进行监控和管理;
- 结果处理：将 Insert、Delete、Search 的执行结果写入 pulsar topic;
- 时钟同步：更新时钟，时钟用于消息缓冲、Segment 状态控制、Insert、Delete 行为正确性保证等。

## 目录结构

```bash
reader/
├── collection.go # Collection 对象
├── index.go # 索引封装，还未开始对接
├── partition.go # Partition 对象
├── query_node.go # Query Node 对象及主要逻辑和接口
├── reader.go # 写节点入口
├── result.go # Query 结果返回
├── segment.go # Segment 对象
└── segment_test.go # Segment 接口测试（进行中）
```

## 主要数据结构

```go
type QueryNode struct {
    QueryNodeId               uint64
	Collections               []*Collection
	messageClient 			  pulsar.MessageClient
	queryNodeTimeSync         *QueryNodeTimeSync
	buffer					  QueryNodeDataBuffer
}

type Collection struct {
	CollectionPtr C.CCollection
	CollectionName string
	Partitions []*Partition
}

type Partition struct {
	PartitionPtr C.CPartition
	PartitionName string
	Segments []*Segment
}

type Segment struct {
	SegmentPtr C.CSegmentBase
	SegmentId	uint64
	SegmentCloseTime uint64
}
```

`QueryNode->Collection->Partition->Segment` 由上到下，即一个 QueryNode 中包含多个 Collection，一个 Collection 中包含多个 Partition，一个 Partition 中包含多个 Segment。
QueryNode、Collection、Partition、Segment 中都有 id 或 name 用于认证和区分。

## 主要接口介绍

```go
func (node *QueryNode) Insert(insertMessages []*schema.InsertMsg, wg *sync.WaitGroup) schema.Status;

func (node *QueryNode) Delete(deleteMessages []*schema.DeleteMsg, wg *sync.WaitGroup) schema.Status;

func (node *QueryNode) Search(searchMessages []*schema.SearchMsg, wg *sync.WaitGroup) schema.Status;

func (node *QueryNode) doQueryNode (wg *sync.WaitGroup);
```

Insert、Delete、Search 在 doQueryNode 中被调用，对每一批从 Pulsar 中接受的消息执行相应的计算。

```go
func (node *QueryNode) SegmentService();
```

额外的线程，用于 Segments 的管理及状态监控。
