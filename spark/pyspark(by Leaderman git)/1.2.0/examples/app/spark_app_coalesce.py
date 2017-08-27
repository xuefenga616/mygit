from pyspark import SparkConf, SparkContext

# Return a new RDD that is reduced into numPartitions partitions.
conf = SparkConf().setAppName("spark_app_coalesce")

sc = SparkContext(conf=conf)

rdd = sc.parallelize([1, 2, 3], 5)

datas = rdd.glom().collect()

datas2 = rdd.coalesce(3).glom().collect()

sc.stop()

print "datas:", datas
print "datas2:", datas2
