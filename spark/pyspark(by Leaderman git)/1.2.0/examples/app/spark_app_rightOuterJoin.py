from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_rightOuterJoin")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([("a", 1), ("a", 2), ("b", 1)])

rdd2 = sc.parallelize([("a", 3), ("c", 1)])

datas = rdd1.rightOuterJoin(rdd2).collect()

sc.stop()

# [('a', (1, 3)), ('a', (2, 3)), ('c', (None, 1))]
print datas
