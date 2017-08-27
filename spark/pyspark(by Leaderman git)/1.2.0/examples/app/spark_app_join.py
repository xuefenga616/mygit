from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_join")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([("a", 1), ("b", 1)])

rdd2 = sc.parallelize([("a", 2), ("a", 3), ("c", 1)])

datas = rdd1.join(rdd2).collect()

sc.stop()

# [('a', (1, 2)), ('a', (1, 3))]
print datas
