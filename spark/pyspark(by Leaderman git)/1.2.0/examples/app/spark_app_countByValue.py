from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_countByValue")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 2, 3, 3, 3]).countByValue()

sc.stop()

for key, val in datas.iteritems():
    print "key:", key, ", val", val
