from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_top")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3, 4, 5]).top(num=1, key=lambda val: val)

sc.stop()

# [5]
print datas
