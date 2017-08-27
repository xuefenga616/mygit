from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row

conf = SparkConf().setAppName("spark_sql_dataframe_where_or_filter")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

lines = sc.parallelize(["a,1", "b,2", "c,3"])

people = lines.map(lambda line: line.split(",")).map(
    lambda words: Row(name=words[0], age=int(words[1])))

schemaPeople = sqlCtx.createDataFrame(people)

schemaPeople.where("name = 'b'").where(schemaPeople["age"] > 1).show()

schemaPeople.where("age > 1").where(schemaPeople["name"] == "b").show()

schemaPeople.where("(name = 'b' or name = 'c') and age >= 2").show()

schemaPeople.where(
    ~(((schemaPeople["name"] == "b") | (schemaPeople["name"] == "c")) & (schemaPeople["age"] >= 2))).show()

sc.stop()
