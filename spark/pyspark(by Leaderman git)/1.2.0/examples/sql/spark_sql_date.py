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


datas = hc.sql(
    "select from_unixtime(cast(round('',0) as bigint)) from temp_source").collect()


def printRows(rows):
    for row in rows:
        print row

printRows(datas)

sc.stop()
