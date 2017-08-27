from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row
import random

conf = SparkConf().setAppName("spark_app_group_top")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

data = ["product" + str(random.randint(1, 10)) + " url" +
        str(random.randint(1, 100)) for index in xrange(1000)]

table = sc.parallelize(data)

tableRDD = table.map(lambda line: line.split(" ")).map(
    lambda words: Row(product=words[0], url=words[1]))

tableSchema = sqlCtx.inferSchema(tableRDD)

tableSchema.registerTempTable("product_url")

accessRDD = sqlCtx.sql(
    "select product, url, count(*) as access from product_url group by product, url")


accessPairRDD = accessRDD.map(lambda row: (
    (row.product, row.url, row.access), None))


def partitionFunc(key):
    return int(key[0][7]) - 1


def keyFunc(key):
    return key[2]


repartitionAndSortRDD = accessPairRDD.repartitionAndSortWithinPartitions(
    numPartitions=10, partitionFunc=partitionFunc, ascending=False, keyfunc=keyFunc)


def topTenFunc(iter):
    buffer = []

    for pair in iter:
        if len(buffer) >= 10:
            break

        buffer.append(pair[0])

    return buffer

rows = repartitionAndSortRDD.mapPartitions(topTenFunc).collect()


rows = sorted(rows, lambda rowA, rowB: cmp(rowA[1], rowB[1]) if not cmp(
    rowA[0], rowB[0]) else cmp(rowA[0], rowB[0]))

for row in rows:
    print row


sc.stop()
