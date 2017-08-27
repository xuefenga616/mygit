from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, StructType, StructField, StringType

conf = SparkConf().setAppName("spark_sql_delimiter_specify_schema")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize(["row1_col1 row1_col2 row1_col3",
                         "row2_col1 row2_col2 row3_col3", "row3_col1 row3_col2 row3_col3"])

columns = source.map(lambda line: line.split(" ")).filter(
    lambda columns: columns and len(columns) == 3)

rows = columns.map(
    lambda columns: (columns[0], columns[1], columns[2]))

schema = StructType([StructField("col1", StringType(), False), StructField(
    "col2", StringType(), False), StructField("col3", StringType(), False)])

table = hc.applySchema(rows, schema)

table.registerAsTable("temp_mytable")

datas = hc.sql("select * from temp_mytable").collect()

sc.stop()

if datas:
    for data in datas:
        print data
