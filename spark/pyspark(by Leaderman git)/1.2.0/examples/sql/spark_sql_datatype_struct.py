# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import StructType, StructField, IntegerType, FloatType, StringType

conf = SparkConf().setAppName("spark_sql_datatype_struct")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize([((1, 2.0, "3.0"),)])

schema = StructType([StructField("struct", StructType([StructField("first", IntegerType(), False), StructField(
    "second", FloatType(), False), StructField("third", StringType(), False)]), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select struct.first, struct.second, struct.third from temp_table").collect()

sc.stop()

for row in rows:
    print row
