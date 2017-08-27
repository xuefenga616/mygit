from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_stats")

sc = SparkContext(conf=conf)

data = sc.parallelize([1, 2, 3]).stats()

sc.stop()

# 3 2.0 0.816496580928 3.0 1.0
print data.count(), data.mean(), data.stdev(), data.max(), data.min()
