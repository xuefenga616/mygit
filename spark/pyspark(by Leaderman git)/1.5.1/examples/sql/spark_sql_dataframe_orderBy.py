from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row, functions

conf = SparkConf().setAppName("spark_sql_dataframe_groupBy")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

lines = sc.parallelize(["m1,d1,1", "m1,d2,2", "m2,d1,1", "m2,d2,2"])

record = lines.map(lambda line: line.split(",")).map(
    lambda columns: Row(machine=columns[0], domain=columns[1], request=columns[2]))

recordSchema = sqlCtx.createDataFrame(record)

recordSchema.orderBy("request", ascending=False).show()

recordSchema.select(
    "machine", "domain", recordSchema.request.cast("int").alias("request")).groupBy("machine", "domain").agg({"request": "max"}).orderBy("max(request)", ascending=False).show()

sc.stop()
