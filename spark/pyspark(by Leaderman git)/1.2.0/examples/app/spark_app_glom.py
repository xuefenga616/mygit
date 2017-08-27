from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_glom")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3], 3).glom().collect()

datas2 = sc.parallelize([1, 2, 3], 6).glom().collect()

sc.stop()

print "datas:", datas
print "datas2:", datas2
