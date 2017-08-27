from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_zipWithUniqueId")

sc = SparkContext(conf=conf)

data = sc.parallelize(["a", "b", "c", "d", "e"], 3).zipWithUniqueId().collect()

sc.stop()

# [('a', 0), ('b', 1), ('c', 4), ('d', 2), ('e', 5)]
print data
