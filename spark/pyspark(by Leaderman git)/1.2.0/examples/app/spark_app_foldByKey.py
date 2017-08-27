from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setAppName("spark_app_foldByKey")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("a", 1), ("b", 1), ("b", 2), ("c", 1), ("c", 2), ("c", 3)]).foldByKey(0, add).collect()

sc.stop()

# [('a', 1), ('c', 6), ('b', 3)]
print datas
