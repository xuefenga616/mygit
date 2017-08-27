from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_keys")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("a", 1), ("a", 2), ("b", 1), ("c", 1)]).keys().collect()

sc.stop()

# ['a', 'a', 'b', 'c']
print datas
