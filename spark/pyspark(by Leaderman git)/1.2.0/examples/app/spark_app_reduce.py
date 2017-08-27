from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setAppName("spark_app_reduce")

sc = SparkContext(conf=conf)

data = sc.parallelize([1, 2, 3]).reduce(add)

sc.stop()

# 6
print data
