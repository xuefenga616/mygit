from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext

conf = SparkConf().setAppName("xinqi_group")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

spark_sql = """select count(*) from datacubic.www_sinaedgeahsolci14ydn_nginx where log_dir='20150915160000'"""

rows = hc.sql(spark_sql).collect()

sc.stop()

print rows
