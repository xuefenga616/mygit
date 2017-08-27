from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_aggregate")

sc = SparkContext(conf=conf)

seqOp = lambda x, y: x + y
combOp = lambda x, y: x + y

data = sc.parallelize([1, 2, 3, 4]).aggregate(0, seqOp, combOp)

seqOp = lambda x, y: (x[0] + y, x[1] + 1)

combOp = lambda x, y: (x[0] + y[0], x[1] + y[1])

data2 = sc.parallelize([1, 2, 3, 4]).aggregate((0, 0), seqOp, combOp)

data3 = sc.parallelize([]).aggregate((0, 0), seqOp, combOp)

sc.stop()

print "data:", data
print "data2:", data2
print "data3:", data3
