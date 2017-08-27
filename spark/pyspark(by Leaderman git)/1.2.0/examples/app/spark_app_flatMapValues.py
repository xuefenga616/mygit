from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_flatMapValues")

sc = SparkContext(conf=conf)


def toUpper(l):
    for index in range(0, len(l)):
        l[index] = l[index].upper()

    return l

datas = sc.parallelize(
    [("key1", ["a", "b", "c"]), ("key2", ["d", "e", "f"])]).flatMapValues(toUpper).collect()

sc.stop()

# datas: [('key1', 'A'), ('key1', 'B'), ('key1', 'C'), ('key2', 'D'),
# ('key2', 'E'), ('key2', 'F')]
print "datas:", datas
