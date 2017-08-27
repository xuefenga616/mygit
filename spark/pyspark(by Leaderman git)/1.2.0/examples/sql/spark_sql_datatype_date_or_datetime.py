# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from datetime import datetime, date
from pyspark.sql import StructType, StructField, DateType, TimestampType

conf = SparkConf().setAppName("spark_sql_datatype_date_or_datetime")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(
    [(date(2015, 9, 22), datetime(2015, 9, 22, 9, 39, 45))])

schema = StructType([StructField("date", DateType(), False),
                     StructField("timestamp", TimestampType(), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select date, timestamp from temp_table").collect()

sc.stop()

for row in rows:
    print row
