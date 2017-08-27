from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row

conf = SparkConf().setAppName("spark_sql_cache")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

rows = hc.sql("select func.ipToLocationBySina('10.13.4.44') from yurun.tablep").collect()

sc.stop()

for row in rows:
    print row
