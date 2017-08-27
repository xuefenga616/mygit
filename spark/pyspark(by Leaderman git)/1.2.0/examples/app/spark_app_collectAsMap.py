from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_collectAsMap")

sc = SparkContext(conf=conf)

items = sc.parallelize([("a", 1), ("b", 2), ("c", 3)]).collectAsMap()

sc.stop()

for key, val in items.iteritems():
    print "key:", key, ", val:", val
