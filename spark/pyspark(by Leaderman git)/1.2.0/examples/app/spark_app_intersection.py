from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_intersection")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([1, 2, 3, 4, 5, 6])

rdd2 = sc.parallelize([2, 4, 6])

datas = rdd1.intersection(rdd2).collect()

sc.stop()

# [2, 4, 6]
print datas
