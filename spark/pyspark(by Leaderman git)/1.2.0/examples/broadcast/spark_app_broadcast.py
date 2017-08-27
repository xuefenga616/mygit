# coding: utf-8

from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_broadcast")

sc = SparkContext(conf=conf)

maps = {"key1": "val1", "key2": "val2", "key3": "other"}

brMaps = sc.broadcast(maps)

keys = sc.parallelize(["key1", "key2", "key3"])

vals = keys.map(lambda e: brMaps[e]).collect()

sc.stop()

for val in vals:
    print val
