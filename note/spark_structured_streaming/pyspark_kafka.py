from pyspark.sql import SparkSession
# from pyspark.sql.functions import explode
# from pyspark.sql.functions import split

import time

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    # batched qurey
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
    # test result
    # --- 16.6633448601 seconds ---
    # +--------+
    # |count(1)|
    # +--------+
    # |10000000|
    # +--------+

    # # Streaming query
    # df = spark \
    # .readStream \
    # .format("kafka") \
    # .option("kafka.bootstrap.servers", "localhost:9092") \
    # .option("subscribe", "test") \
    # .load() \
    # .selectExpr("CAST(value AS STRING)")
    # df.writeStream \
    # .format("console") \
    # .trigger(processingTime='5 seconds') \
    # .start() \
    # .awaitTermination()
