# coding=utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row

conf = SparkConf().setAppName("spark_sql_cache")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(
    ['{"col1": "row1_col1","col2":"row1_col2","col3":"row1_col3"}', '{"col1": "row2_col1","col2":"row2_col2","col3":"row2_col3"}', '{"col1": "row3_col1","col2":"row3_col2","col3":"row3_col3"}'])


sourceRDD = hc.jsonRDD(source)

sourceRDD.registerTempTable("temp_source")

"""
def convert(row):
    mydict = row.asDict()

    mydict["col1"] = mydict["col1"].upper()

    return Row(**mydict)

convertRDD = hc.sql(
    "select col1, col2, col3 from temp_source").map(convert)

mytable = hc.inferSchema(convertRDD)

mytable.registerTempTable("temp_mytable")
"""


def convert(val):
    return val.upper()

hc.registerFunction("temp_convert", convert)

convertRDD = hc.sql(
    "select temp_convert(col1) as col1, col2, col3 from temp_source")

convertRDD.registerAsTable("temp_mytable")


hc.cacheTable("temp_mytable")


def printRows(rows):
    for row in rows:
        print row

datas = hc.sql("select * from temp_mytable").collect()

printRows(datas)

datas = hc.sql("select col1 from temp_mytable").collect()

printRows(datas)

# hc.uncacheTable("temp_mytable")

sc.stop()
