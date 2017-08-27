from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_groupWith")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([("a", 1), ("a", 2), ("b", 1)])
rdd2 = sc.parallelize([("a", 3), ("b", 2), ("c", 1)])
rdd3 = sc.parallelize([("c", 2), ("d", 1)])

datas = rdd1.groupWith(rdd2, rdd3).collect()

sc.stop()

# [('b', ([1], [2], [])), ('d', ([], [], [1])), ('a', ([1, 2], [3], [])), ('c', ([], [1], [2]))]
print[(x, (list(y[0]), list(y[1]), list(y[2]))) for x, y in datas]
