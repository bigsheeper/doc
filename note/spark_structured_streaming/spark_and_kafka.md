# 基于 Kafka 的 Spark Structured Streaming

本文档介绍如何基于 Kafka 在 Scala 和 Python 两个层面进行 Spark Structured Streaming 操作，同时比较 Spark Structured Streaming 的 Python 与 Scala 在大规模数据情况下的性能。

## 安装与部署

介绍 Kafka 与 Spark Structured Streaming 的安装与部署流程。

### 安装部署 Kafka

下载 kafka_2.12-2.5.0 并解压：

``` bash
> wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.5.0/kafka_2.12-2.5.0.tgz
> tar -xzf kafka_2.12-2.5.0.tgz
> cd kafka_2.12-2.5.0
```

在不同的终端下启动 ZooKeeper Server 与 Kafka Server：

```bash
> bin/zookeeper-server-start.sh config/zookeeper.properties
> bin/kafka-server-start.sh config/server.properties
```

在不同的终端下创建 topic，此处创建一个名为 test 的 topic：

```bash
> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
```

在不同的终端下向 test 发送一些 message：

```bash
> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test
This is a message
This is another message
```

在不同的终端下使用 Kafka consumer 接收发送的信息，若能看到与发送的 message 一样的输出，则说明 Kafka 安装部署成功：

```bash
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
This is a message
This is another message
```

### 安装部署 Spark Structured Streaming

Spark Structured Streaming 是基于 Spark SQL 引擎上的可扩展和具有容错性的流处理引擎。因此我们只需要下载并解压 Spark-2.4.5 的二进制版本便可直接使用 Spark Structured Streaming：

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
tar -zxf spark-2.4.5-bin-hadoop2.7.tgz
cd spark-2.4.5-bin-hadoop2.7
```

## 项目搭建与运行

搭建 Kafka 与基于 Scala 和 Python 的 Spark Structured Streaming 平台。

### 搭建 Kafka

先启动 ZooKeeper Server 与 Kafka Server，并创建 test topic。使用如下命令给 test 中发送深圳运营车辆的所有消息（此处使用 1000 万行的深圳运营车辆 CSV 文件，你也可以使用自己的其他 CSV 文件）：

```bash
> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test < sz_1000w.csv
```

使用如下命令查看 test topic 中的 message 数量：

```bash
> bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test --time -1
test:0:10000000
```

### 在 Scala 环境下搭建运行 Spark Structured Streaming

创建 Scala Project，并给 build.sbt 中添加相关依赖：

```scala
libraryDependencies ++= Seq("org.apache.spark" % "spark-sql_2.11" % "2.4.5",
  "org.apache.spark" % "spark-sql-kafka-0-10_2.11" % "2.4.5",
  "org.apache.kafka" % "kafka-clients" % "0.11.0.1")
```

创建测试对象 PerfTest：

```scala
import org.apache.spark.sql.SparkSession

object PerfTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder
      .appName("Spark-Kafka-Integration")
      .master("local")
      .getOrCreate()

    val t1 = System.currentTimeMillis

    val df = spark
      .read
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "test")
      .load()
      .selectExpr("CAST(value AS STRING)")

    df.createOrReplaceTempView("df")
    spark.sql("cache table df")

    val t2 = System.currentTimeMillis
    println((t2 - t1) / 1000.0 + " secs")

    val res = spark.sql("select count(*) from df")
    res.show()
  }
}
```

若你是在 IntelliJ 中搭建的此项目，则 build 并运行 main 函数即可; 若你是在终端中搭建的此项目，则在项目主目录中使用如下命令 build 和运行：

```bash
# build project
$ sbt

# 在 scala shell 中：
sbt:spark_kafka> ~run
```

以上项目代码可见 <https://github.com/bigsheeper/sheep_scala/tree/master/spark_kafka>。

### 在 Python 环境下搭建运行 Spark Structured Streaming

编写将要运行的 Pyspark 脚本，代码如下：

```python
from pyspark.sql import SparkSession
import time

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    start_time = time.time()

    df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

    df.createOrReplaceTempView("df")
    spark.sql("cache table df")

    print("--- %s seconds ---" % (time.time() - start_time))

    res = spark.sql("select count(*) from df")
    res.show()
```

使用如下命令运行此 Pyspark 脚本（注意，由于 spark-2.4.5 是由 scala-2.11 编译的，因此需要将官网给的依赖包的 scala 版本由 2.12 改为 2.11）：

```bash
spark-2.4.5-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 pyspark_kafka.py
```

## 测试结果

在 Scala 环境下的测试打印结果：

```scala
// 16.986 secs
// +--------+
// |count(1)|
// +--------+
// |10000000|
// +--------+
```

在 Python 环境下的测试打印结果：

```python
# --- 16.6633448601 seconds ---
# +--------+
# |count(1)|
# +--------+
# |10000000|
# +--------+
```

## 参考链接

Kafka：

<https://kafka.apache.org/quickstart>
<https://kafka.apache.org/intro>

Spark Structured Streaming：

<https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html>
<https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html>
