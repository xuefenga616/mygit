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

conf = SparkConf().setAppName("spark_sql_datatype_extend3")

sc = SparkContext(conf=conf)

source = sc.parallelize(
    ["85070591730234615847396907784232501249", "85070591730234615847396907784232501249"])

result = source.map(lambda value: long(value)).reduce(
    lambda valA, valB: valA + valB)

sc.stop()

print result, type(result)
