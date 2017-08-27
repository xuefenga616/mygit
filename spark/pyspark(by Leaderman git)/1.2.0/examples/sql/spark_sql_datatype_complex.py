# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import StructType, StructField, ArrayType, MapType

conf = SparkConf().setAppName("spark_sql_datatype_complex")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize([([1, 2, 3], {"key1": 1, "key2": 2}, (1, 2.0, "3.0"))])

schema = StructType([StructField("array", ArrayType(IntegerType(), False), False), StructField("col_map", MapType(StringType(), IntegerType(), False), False), StructField(
    "struct", StructType([StructField("first", IntegerType(), False), StructField("second", FloatType(), False), StructField("third", StringType(), False)]), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select array[0], array[1], array[2], col_map['key1'], col_map['key2'], struct.first, struct.second, struct.third from temp_table").collect()

sc.stop()

for row in rows:
    print row
