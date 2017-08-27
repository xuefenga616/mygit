from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_map")

sc = SparkContext(conf=conf)

datas = sc.parallelize(["a", "b", "c"]).map(lambda val: val.upper()).collect()

sc.stop()

# ['A', 'B', 'C']
print datas
