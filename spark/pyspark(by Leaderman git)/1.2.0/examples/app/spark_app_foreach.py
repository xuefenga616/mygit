from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_foreach")

sc = SparkContext(conf=conf)


def log(val):
    print "val:", val

sc.parallelize(["a", "b", "c"]).foreach(log)

sc.stop()
