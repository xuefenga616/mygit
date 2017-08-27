from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row
from pyspark.sql.types import StringType

conf = SparkConf().setAppName("spark_sql_udf")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

lines = sc.parallelize(["a", "b", "c"])

people = lines.map(lambda value: Row(name=value))

peopleSchema = hc.inferSchema(people)

peopleSchema.registerTempTable("people")


def myfunc(value):
    return value.upper()

hc.registerFunction("myfunc", myfunc, StringType())

rows = hc.sql("select myfunc(name) from people").rdd.filter(
    lambda row: isinstance(row, tuple)).collect()

sc.stop()

for row in rows:
    print row, type(row[0])
