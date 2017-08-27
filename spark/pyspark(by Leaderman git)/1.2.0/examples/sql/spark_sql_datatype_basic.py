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
from decimal import Decimal
from datetime import datetime, date
from pyspark.sql import StructType, StructField, ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType, StringType, BooleanType, TimestampType, DateType, ArrayType, MapType

conf = SparkConf().setAppName("spark_sql_datatype_basic")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

"""
source = sc.parallelize([(-128, 127)])

schema = StructType([StructField("col1", ByteType(), False),
                     StructField("col2", ByteType(), False)])
"""

"""
source = sc.parallelize([(-32768, 32767)])

schema = StructType([StructField("col1", ShortType(), False),
                     StructField("col2", ShortType(), False)])
"""

"""
source = sc.parallelize(
    [(-2147483648, 2147483647)])

schema = StructType([StructField("col1", IntegerType(), False),
                     StructField("col2", IntegerType(), False)])
"""

"""
source = sc.parallelize(
    [(-9223372036854775808, 9223372036854775807)])

schema = StructType([StructField("col1", LongType(), False),
                     StructField("col2", LongType(), False)])
"""

"""
source = sc.parallelize(
    [(1.4E-45, 3.4028235E38)])

schema = StructType([StructField("col1", FloatType(), False),
                     StructField("col2", FloatType(), False)])
"""

"""
source = sc.parallelize(
    [(4.9E-324, 1.7976931348623157E308)])

schema = StructType([StructField("col1", DoubleType(), False),
                     StructField("col2", DoubleType(), False)])
"""

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql(
    "select col1 + col2 from temp_table").collect()

sc.stop()

for row in rows:
    print row
