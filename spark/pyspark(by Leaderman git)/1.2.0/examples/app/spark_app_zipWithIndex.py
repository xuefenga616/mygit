from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_zipWithIndex")

sc = SparkContext(conf=conf)

data = sc.parallelize(["a", "b", "c", "d"], 3).zipWithIndex().collect()

sc.stop()

# [('a', 0), ('b', 1), ('c', 2), ('d', 3)]
print data
