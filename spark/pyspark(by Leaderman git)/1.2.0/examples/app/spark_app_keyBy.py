from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_keyBy")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3, 4, 5]).keyBy(lambda val: val ** 3).collect()

sc.stop()

# [(1, 1), (8, 2), (27, 3), (64, 4), (125, 5)]
print datas
