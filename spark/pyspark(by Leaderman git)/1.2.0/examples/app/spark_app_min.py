from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_min")

sc = SparkContext(conf=conf)

data = sc.parallelize([1, 2, 3]).min()

data2 = sc.parallelize([("a", 1), ("b", 2), ("c", 3)]).min(lambda val: val[1])

sc.stop()

# 1 ('a', 1)
print data, data2
