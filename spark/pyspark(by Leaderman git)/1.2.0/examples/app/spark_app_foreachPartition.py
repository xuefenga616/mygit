import time
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_foreachPartition")

sc = SparkContext(conf=conf)


def log(iterator):
    for val in iterator:
    	time.sleep(60)

        print val

sc.parallelize([1, 2, 3, 4, 5]).coalesce(1).foreachPartition(log)

sc.stop()
