from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_accumulator")

sc = SparkContext(conf=conf)

accum = sc.accumulator(0)

sc.parallelize([0, 1, 2, 3]).foreach(lambda e: accum.add(1))

sc.stop()

print accum.value
