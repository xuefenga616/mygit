from pyspark import SparkConf, SparkContext
import pyhs2

conf = SparkConf().setAppName("spark_app_aggregate")

sc = SparkContext(conf=conf)

rows = ["1\t2\t3", "4\t5\t6", "7\t8\t9"]

data = sc.parallelize(rows)

data.saveAsTextFile("hdfs://testhadoop/user/datacubic/warehouse/pyspark_table/1")

sc.stop()

conn = pyhs2.connect(host = "10.210.136.64", port = 10002, authMechanism = "PLAIN", user = "xinqi", password = "61dcb1418596423988fa9b6c3e32cf3b9gXG6CUD", database = "default")

cur = conn.cursor()

cur.execute("alter table yurun_test add partition (mypartition = '1') location 'hdfs://testhadoop/user/datacubic/warehouse/pyspark_table/1'")

cur.close()

conn.close()