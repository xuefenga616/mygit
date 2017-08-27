from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_mapValues")

sc = SparkContext(conf=conf)

datas = sc.parallelize([("key1", ["a", "b", "c"]), ("key2", ["d"])]).mapValues(
    lambda vals: [val.upper() for val in vals]).collect()

sc.stop()

# [('key1', ['A', 'B', 'C']), ('key2', ['D'])]
print datas
