from pyspark import SparkConf, SparkContext
from operator import add

conf = SparkConf().setAppName("spark_app_reduceByKeyLocally")

sc = SparkContext(conf=conf)

datas = sc.parallelize(
    [("c", 1), ("b", 1), ("a", 2), ("a", 1)]).reduceByKeyLocally(add)

sc.stop()

# {'a': 3, 'c': 1, 'b': 1}
print datas
