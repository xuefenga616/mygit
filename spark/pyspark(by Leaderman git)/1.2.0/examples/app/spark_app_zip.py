from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_zip")

sc = SparkContext(conf=conf)

"""
Assumes that the two RDDs have the same number of partitions and the same number of elements in each partition
"""
x = sc.parallelize(range(0, 5))

y = sc.parallelize(range(1000, 1005))

datas = x.zip(y).collect()

sc.stop()

# [(0, 1000), (1, 1001), (2, 1002), (3, 1003), (4, 1004)]
print datas
