# coding=utf-8

from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.types import Row

conf = SparkConf().setAppName("spark_sql_cache_table_extend")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

dataRDD = sc.textFile("/user/hdfs/rawlog/app_weibomobile03x4ts1kl_mwb_interface/").map(lambda line: line.split(
    ",")).filter(lambda words: len(words) >= 3).map(lambda words: Row(col1=words[0], col2=words[1], col3=words[2]))

sourceRDD = hc.inferSchema(dataRDD)

sourceRDD.registerAsTable("source")

hc.cacheTable("source")

hc.sql("select count(*) from source").collect()

hc.sql("select col2, max(col3) from source group by col2").collect()

hc.sql("select col3, min(col2) from source group by col3").collect()

# hc.uncacheTable("source")

sc.stop()
