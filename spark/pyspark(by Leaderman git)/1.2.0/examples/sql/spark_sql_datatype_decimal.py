# coding: utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from decimal import Decimal
from pyspark.sql.types import StructType, StructField, DecimalType

conf = SparkConf().setAppName("spark_sql_datatype_decimal")

sc = SparkContext(conf=conf)

hc = SQLContext(sc)

source = sc.parallelize(
    [(Decimal("1.0"), Decimal("2.0"))])

schema = StructType([StructField("col1", DecimalType(), False),
                     StructField("col2", DecimalType(), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select col1 + col2, col2 + 1.0 from temp_table").collect()

sc.stop()

for row in rows:
    print row
