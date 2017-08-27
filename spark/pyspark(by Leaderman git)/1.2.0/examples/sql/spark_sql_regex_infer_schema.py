from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row
import re

conf = SparkConf().setAppName("spark_sql_regex_infer_schema")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(["row1_col1 row1_col2 row1_col3",
                         "row2_col1 row2_col2 row3_col3", "row3_col1 row3_col2 row3_col3"])

pattern = re.compile("(.*) (.*) (.*)")


def parse(line):
    matcher = pattern.match(line)

    if matcher:
        return matcher.groups()
    else:
        return None

columns = source.map(parse).filter(
    lambda columns: columns and len(columns) == 3)

rows = columns.map(
    lambda columns: Row(col1=columns[0], col2=columns[1], col3=columns[2]))


table = hc.inferSchema(rows)

table.registerAsTable("temp_mytable")

datas = hc.sql("select * from temp_mytable").collect()

sc.stop()

if datas:
    for data in datas:
        print data
