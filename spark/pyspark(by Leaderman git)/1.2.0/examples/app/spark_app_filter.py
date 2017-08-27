from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_filter")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3, 4, 5]).filter(
    lambda val: val % 2 == 0).collect()

sc.stop()

for data in datas:
    print data
