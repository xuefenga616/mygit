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
from pyspark.sql import StructType, StructField, LongType

conf = SparkConf().setAppName("spark_sql_datatype_extend2")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(
    [(85070591730234615847396907784232501249, 85070591730234615847396907784232501249)])

schema = StructType([StructField("col1", LongType(), False),
                     StructField("col2", LongType(), False)])

table = hc.applySchema(source, schema)

table.registerAsTable("temp_table")

rows = hc.sql("select * from temp_table").collect()

sc.stop()

for row in rows:
    print row


"""
# java.lang.ClassCastException: java.math.BigInteger cannot be cast to
# java.lang.Long
hc.sql(
    "select col1 + col2 from temp_table").collect()
"""
