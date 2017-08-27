# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import StructType, StructField, MapType, StringType, IntegerType

conf = SparkConf().setAppName("spark_sql_datatype_map")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize([({"key1": 1, "key2": 2}, )])

schema = StructType(
    [StructField("col_map", MapType(StringType(), IntegerType(), False), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select col_map['key1'], col_map['key2'] from temp_table").collect()

sc.stop()

for row in rows:
    print row
