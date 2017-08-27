# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
import decimal
from datetime import datetime, date
from pyspark.sql import StructType, StructField, LongType

conf = SparkConf().setAppName("spark_sql_datatype_long")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(
    [(9223372036854775807, 9223372036854775807)])

schema = StructType([StructField("col1", LongType(), False),
                     StructField("col2", LongType(), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

"""
rows = hc.sql("select col1 + col2 from temp_table").collect()
"""

"""
rows = hc.sql(
    "select cast(col1 as bigint) + cast(col2 as bigint) from temp_table").collect()
"""

rows = hc.sql(
    "select cast(col1 as decimal(38, 0)) + cast(col2 as decimal(38, 0)) from temp_table").collect()
    
sc.stop()

for row in rows:
    print row[0], type(row[0])
