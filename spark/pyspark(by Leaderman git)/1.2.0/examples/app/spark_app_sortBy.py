from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_sortBy")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("c", 1), ("b", 1), ("a", 2), ("a", 1)]).sortBy(keyfunc=lambda val: val[1], ascending=False).collect()

sc.stop()

# [('a', 2), ('a', 1), ('b', 1), ('c', 1)]
print datas
