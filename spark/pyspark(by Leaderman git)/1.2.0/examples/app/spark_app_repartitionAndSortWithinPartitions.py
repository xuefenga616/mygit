from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_repartitionAndSortWithinPartitions")

sc = SparkContext(conf=conf)

# only key is passed to paritionFunc(keyfunc)
datas = sc.parallelize([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]).repartitionAndSortWithinPartitions(
    numPartitions=2, partitionFunc=lambda val: val, ascending=False, keyfunc=lambda val: val).glom().collect()

sc.stop()

# [[(4, 'd'), (2, 'b')], [(5, 'e'), (3, 'c'), (1, 'a')]]
print datas
