from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_distinct")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 2, 3, 3, 3]).distinct().collect()

sc.stop()

for data in datas:
    print data
