# coding: utf-8

"""Spark SQL DataType

ByteType: int
ShortType: int
IntegerType: int
LongType: long
FloatType: float
DoubleType: float
Decimal: Decimal
StringType: ""
BinaryType: ignore
BooleanType: bool
TimestampType: datetime
DateType: date
ArrayType: list
MapType: dict
StructType: tuple
"""

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
import decimal
from datetime import datetime, date
from pyspark.sql import StructType, StructField, StringType

conf = SparkConf().setAppName("spark_sql_datatype_div")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(
    [("92233720368547758", "92233720368547758070")])

schema = StructType([StructField("col1", StringType(), False),
                     StructField("col2", StringType(), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select col1, col2, col1 + col2 from temp_table").collect()


"""
rows = hc.sql(
    "select (cast(col1 as decimal(38, 3)) + col2) / 1.0 from temp_table").collect()
"""

sc.stop()

for row in rows:
    print row, type(row[2])
