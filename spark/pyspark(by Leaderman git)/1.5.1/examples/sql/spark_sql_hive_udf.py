from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row

conf = SparkConf().setAppName("spark_sql_hive_udf")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

lines = sc.parallelize(["a", "b", "c"])

people = lines.map(lambda value: Row(name=value))

peopleSchema = hc.inferSchema(people)

peopleSchema.registerTempTable("people")

#rows = hc.sql("select func.ipToLocationBySina('10.13.4.44') from people").collect()

rows = hc.sql("SHOW FUNCTIONS like 'f.*'").collect()

sc.stop()

for row in rows:
    print row, type(row[0])