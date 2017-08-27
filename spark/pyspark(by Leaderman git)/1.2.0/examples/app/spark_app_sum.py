from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_sum")

sc = SparkContext(conf=conf)

data = sc.parallelize([1, 2, 3]).sum()

sc.stop()

# 6
print data
