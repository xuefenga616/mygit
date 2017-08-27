from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_aggregateByKey")

sc = SparkContext(conf=conf)

seqFunc = lambda a, b: a + b
combFunc = seqFunc

datas = sc.parallelize(
    [("a", 1), ("b", 1), ("b", 2), ("c", 1), ("c", 2), ("c", 3)]).aggregateByKey(0, seqFunc, combFunc).collect()

sc.stop()

for data in datas:
    print "key:", data[0], ", value:", data[1]
