from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row, functions

conf = SparkConf().setAppName("spark_sql_dataframe_groupBy")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

lines = sc.parallelize(["m1,d1,1", "m1,d2,2", "m2,d1,1", "m2,d2,2"])

record = lines.map(lambda line: line.split(",")).map(
    lambda columns: Row(machine=columns[0], domain=columns[1], request=columns[2]))

recordSchema = sqlCtx.createDataFrame(record)

recordSchema.groupBy().agg({"*": "count"}).show()

recordSchema.groupBy("machine", recordSchema["domain"]).agg(
    {"domain": "max", "request": "min"}).show()

recordSchema.groupBy("machine", recordSchema.domain).agg(functions.count("*"), functions.max(
    recordSchema.request), functions.min(recordSchema["request"]), functions.sum(recordSchema["request"]), functions.avg(recordSchema["request"])).show()

recordSchema.select(recordSchema.machine, recordSchema.request.cast(
    "int")).groupBy("machine").count().show()

recordSchema.select(recordSchema.machine, recordSchema.request.cast(
    "int").alias("request")).groupBy("machine").max("request").show()

recordSchema.select(recordSchema.machine, recordSchema.request.cast(
    "int").alias("request")).groupBy("machine").min("request").show()

recordSchema.select(recordSchema.machine, recordSchema.request.cast(
    "int").alias("request")).groupBy("machine").sum("request").show()

recordSchema.select(recordSchema.machine, recordSchema.request.cast(
    "int").alias("request")).groupBy("machine").avg("request").show()

sc.stop()
