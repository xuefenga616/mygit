from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row

conf = SparkConf().setAppName("spark_sql_dataframe_select")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

lines = sc.parallelize(["a,1", "b,2", "c,3"])

people = lines.map(lambda line: line.split(",")).map(
    lambda words: Row(name=words[0], age=words[1]))

schemaPeople = sqlCtx.createDataFrame(people)

schemaPeople.select("*").show()

schemaPeople.select("name", "age").show()

schemaPeople.select("name", schemaPeople["age"]).show()

# error schemaPeople.select("name", schemaPeople2["age"]).show()

# error schemaPeople.select("name", "age * 2").show()

schemaPeople.select(schemaPeople["name"].alias(
    "name2"), schemaPeople.age.cast("int").alias("age2")).show()

sc.stop()
