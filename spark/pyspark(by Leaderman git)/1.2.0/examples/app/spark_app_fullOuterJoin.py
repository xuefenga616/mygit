from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_fullOuterJoin")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([("a", 1), ("b", 1), ("a", 3)])

rdd2 = sc.parallelize([("a", 2), ("c", 1)])

datas = rdd1.fullOuterJoin(rdd2).collect()

sc.stop()

# [('a', (1, 2)), ('a', (3, 2)), ('c', (None, 1)), ('b', (1, None))]
print datas
