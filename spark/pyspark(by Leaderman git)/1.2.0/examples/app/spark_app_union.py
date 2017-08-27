from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_union")

sc = SparkContext(conf=conf)

rdd1 = sc.parallelize(["line1", "line2", "line3"])

rdd2 = sc.parallelize(["line4", "line5"])

datas = rdd1.union(rdd2).collect()

sc.stop()

# ['line1', 'line2', 'line3', 'line4', 'line5']
print datas
