# coding: utf-8


from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import StructType, StructField, ArrayType, IntegerType

conf = SparkConf().setAppName("spark_sql_datatype_array")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize([([1, 2, 3], )])

schema = StructType(
    [StructField("array", ArrayType(IntegerType(), False), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select array[0], array[1], array[2] from temp_table").collect()

sc.stop()

for row in rows:
    print row
