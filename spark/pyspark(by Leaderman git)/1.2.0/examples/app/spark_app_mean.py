from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_mean")

sc = SparkContext(conf=conf)

data = sc.parallelize([1, 2, 3]).mean()

sc.stop()

# 2.0
print data
