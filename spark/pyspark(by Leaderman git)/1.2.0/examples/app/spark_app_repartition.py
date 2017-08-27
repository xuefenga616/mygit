from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_repartition")

sc = SparkContext(conf=conf)

rdd = sc.parallelize([1, 2, 3], 3)

datas = rdd.glom().collect()

datas2 = rdd.repartition(5).glom().collect()

sc.stop()

# datas: [[1], [2], [3]]
print "datas:", datas

# datas2: [[], [1, 2], [], [], [3]]
print "datas2:", datas2
