from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_mapPartitionsWithIndex")

sc = SparkContext(conf=conf)


def f(index, vals):
    yield index

datas = sc.parallelize([1, 2, 3, 4, 5], 3).mapPartitionsWithIndex(f).collect()

sc.stop()

# [0, 1, 2]
print datas
