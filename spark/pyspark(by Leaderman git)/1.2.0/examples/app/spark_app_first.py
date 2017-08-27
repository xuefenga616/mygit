from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_first")

sc = SparkContext(conf=conf)

data = sc.parallelize([1, 2, 3]).first()

# ValueError: RDD is empty
#data2 = sc.parallelize([]).first()

sc.stop()

print data
