from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_groupBy")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3, 4, 5]).groupBy(lambda val: val % 2).collect()

sc.stop()

# [(0, [2, 4]), (1, [1, 3, 5])]
print[(x, list(y)) for x, y in datas]
