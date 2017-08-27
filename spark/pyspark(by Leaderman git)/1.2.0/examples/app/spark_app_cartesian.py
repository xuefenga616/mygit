from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_cartesian")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize([1, 2])

rdd2 = sc.parallelize([1, 2, 3])

datas = rdd1.cartesian(rdd2).collect()

sc.stop()

for data in datas:
    print data
