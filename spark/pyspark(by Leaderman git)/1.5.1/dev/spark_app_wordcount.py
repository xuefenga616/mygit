import time
from pyspark import SparkConf, SparkContext

conf = SparkConf()

conf.setAppName("spark_app_wordcount")

sc = SparkContext(conf=conf)

lines = sc.parallelize(["row1_col1 row1_col2 row1_col3",
                        "row2_col1 row2_col2 row3_col3", "row3_col1 row3_col2 row3_col3"])

words = lines.flatMap(lambda line: line.split(" "))

words = words.coalesce(30)

pairs = words.map(lambda word: (word, 1))

counts = pairs.reduceByKey(lambda a, b: a + b)

counts = counts.coalesce(1)


def log(iterator):
    for val in iterator:
        time.sleep(30)


counts.foreachPartition(log)

sc.stop()
