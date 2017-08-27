from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setAppName("spark_app_reduceByKey")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("c", 1), ("b", 1), ("a", 2), ("a", 1)]).reduceByKey(add).collect()

sc.stop()

# [('a', 3), ('c', 1), ('b', 1)]
print datas
