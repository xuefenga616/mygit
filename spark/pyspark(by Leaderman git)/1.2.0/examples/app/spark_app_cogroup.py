from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_cogroup")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([("a", 1), ("a", 2), ("b", 1)])

rdd2 = sc.parallelize([("a", 2), ("b", 2),  ("b", 3), ("c", 2)])

datas = rdd1.cogroup(rdd2).collect()

sc.stop()

"""
a ([1, 2], [2])
c ([], [2])
b ([1], [2, 3])
"""
for data in datas:
    print data[0], (list(data[1][0]), list(data[1][1]))
