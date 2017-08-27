from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_flatMap")

sc = SparkContext(conf=conf)

rdd = sc.parallelize([1, 2, 3])

datas = rdd.flatMap(lambda val: [val, val + 1, val + 2]).collect()

datas2 = rdd.flatMap(lambda val: [[val, val, val], [
                     val + 1, val + 1, val + 1], [val + 2, val + 2, val + 2]]).collect()

sc.stop()

# datas: [1, 2, 3, 2, 3, 4, 3, 4, 5]
print "datas:", datas

# datas2: [[1, 1, 1], [2, 2, 2], [3, 3, 3], [2, 2, 2], [3, 3, 3], [4, 4,
# 4], [3, 3, 3], [4, 4, 4], [5, 5, 5]]
print "datas2:", datas2
