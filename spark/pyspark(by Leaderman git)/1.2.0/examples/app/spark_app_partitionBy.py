from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_partitionBy")

sc = SparkContext(conf=conf)

# only key is passed to paritionFunc
datas = sc.parallelize([1, 2, 3, 4, 5]).map(lambda val: (val, val)).partitionBy(
    2, lambda val: val).map(lambda val: val[0]).glom().collect()

sc.stop()

# [[2, 4], [1, 3, 5]]
print datas
