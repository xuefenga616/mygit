# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import StructType, StructField, StringType, BooleanType, BinaryType, NullType

conf = SparkConf().setAppName("spark_sql_datatype_str_bool_binary_none")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize([("str", False, bytearray(range(0, 256)), None)])

schema = StructType([StructField("str", StringType(), False), StructField("bool", BooleanType(
), False), StructField("bytes", BinaryType(), False), StructField("none", NullType())])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select str, bool, bytes, none from temp_table").collect()

sc.stop()

for row in rows:
    print row
