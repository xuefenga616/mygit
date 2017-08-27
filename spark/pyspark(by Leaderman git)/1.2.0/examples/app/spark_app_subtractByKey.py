from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_subtractByKey")

sc = SparkContext(conf=conf)

x = sc.parallelize([("a", 1), ("b", 4), ("b", 5), ("a", 3)])

y = sc.parallelize([("a", 3), ("c", None)])

datas = x.subtractByKey(y).collect()

sc.stop()

# [('b', 4), ('b', 5)]
print datas
