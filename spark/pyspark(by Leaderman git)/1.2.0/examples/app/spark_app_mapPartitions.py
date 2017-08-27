from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_mapPartitions")

sc = SparkContext(conf=conf)


def f(vals):
    yield sum(vals)

datas = sc.parallelize([1, 2, 3, 4, 5], 3).mapPartitions(f).collect()

sc.stop()

# [1, 5, 9]
print datas
