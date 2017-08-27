from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_take")

sc = SparkContext(conf=conf)

rdd = sc.parallelize([1, 2, 3])

data = sc.parallelize([]).take(1)

data2 = rdd.take(2)

data3 = rdd.take(4)

# ValueError: RDD is empty
#data2 = sc.parallelize([]).first()

sc.stop()

# []
print data

# [1, 2]
print data2

# [1, 2, 3]
print data3
