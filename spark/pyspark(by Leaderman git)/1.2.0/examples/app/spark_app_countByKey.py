from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_countByKey")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("a", 1), ("b", 1), ("b", 2), ("c", 1), ("c", 2), ("c", 3)]).countByKey()

sc.stop()

for key, val in datas.iteritems():
    print "key:", key, ", val:", val
