from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

conf = SparkConf().setAppName("spark_sql_hive")

conf.set("hive.metastore.uris", "thrift://10.13.4.44:9083")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

try:
    rows = hc.sql("select count(1) from yurun_test").collect()

    print rows
except Exception, e:
    print e
finally:
    pass


sc.stop()
