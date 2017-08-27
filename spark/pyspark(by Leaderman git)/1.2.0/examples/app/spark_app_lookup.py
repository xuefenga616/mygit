from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_lookup")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("a", 1), ("a", 2), ("a", 3), ("b", 1), ("c", 1)]).sortByKey().lookup("a")

sc.stop()

# [1, 2, 3]
print datas
