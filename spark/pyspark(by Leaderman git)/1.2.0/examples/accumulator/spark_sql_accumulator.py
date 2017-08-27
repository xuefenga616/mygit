# coding: utf-8

"""
Spark SQL使用Accumulator时存在误差，因为需要抽取一定数目（10）的“行”校验数据模式，以下代码的输出结果：

allLines: 110
successLines: 60
errorLines:  50
"""

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row, StructType, StructField, StringType

conf = SparkConf().setAppName("spark_app_accumulator")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

allLines = sc.accumulator(0)
successLines = sc.accumulator(0)
errorLines = sc.accumulator(0)

datas = []

"""50行正确的数据"""
for index in range(50):
    datas.append("col1 col2 col3")

"""50行错误的数据"""
for index in range(50):
    datas.append("col1col2col3")

source = sc.parallelize(datas)


def lineFilter(columns):
    allLines.add(1)

    if columns and len(columns) == 3:
        successLines.add(1)

        return True
    else:
        errorLines.add(1)

        return False

columns = source.map(lambda line: line.split(" ")).filter(lineFilter)

rows = columns.map(
    lambda columns: (columns[0], columns[1], columns[2]))

schema = StructType([StructField("col1", StringType()), StructField(
    "col2", StringType()), StructField("col3", StringType())])

table = hc.applySchema(rows, schema)

table.registerAsTable("temp_mytable")

datas = hc.sql("select * from temp_mytable").collect()

sc.stop()

if datas:
    for data in datas:
        print data

print "allLines:", allLines.value
print "successLines:", successLines.value
print "errorLines: ", errorLines.value
