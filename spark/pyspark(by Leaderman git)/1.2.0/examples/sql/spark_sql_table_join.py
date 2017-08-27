from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row

conf = SparkConf().setAppName("spark_sql_table_join")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

line1 = sc.parallelize(["name1 a", "name3 c", "name4 d"])

line2 = sc.parallelize(["name1 1", "name2 2", "name3 3"])

word1 = line1.map(lambda line: line.split(" "))

word2 = line2.map(lambda line: line.split(" "))

table1 = word1.map(lambda words: Row(name=words[0], title=words[1]))

table2 = word2.map(lambda words: Row(name=words[0], fraction=words[1]))

tableSchema1 = sqlCtx.inferSchema(table1)

tableSchema2 = sqlCtx.inferSchema(table2)

tableSchema1.registerTempTable("table1")

tableSchema2.registerTempTable("table2")


def printRows(rows):
    if rows:
        for row in rows:
            print row

# inner join
rows = sqlCtx.sql(
    "select table1.name, table1.title, table2.fraction from table1 join table2 on table1.name = table2.name").collect()

printRows(rows)

print "============================================="

# left outer join
rows = sqlCtx.sql(
    "select table1.name, table1.title, table2.fraction from table1 left outer join table2 on table1.name = table2.name").collect()

printRows(rows)

# right outer join
rows = sqlCtx.sql(
    "select table1.name, table1.title, table2.fraction from table1 right outer join table2 on table1.name = table2.name").collect()

print "============================================="

printRows(rows)

# full outer join
rows = sqlCtx.sql(
    "select table1.name, table1.title, table2.fraction from table1 full outer join table2 on table1.name = table2.name").collect()

print "============================================="

printRows(rows)

"""
Row(name=u'name1', title=u'a', fraction=u'1')                                   
Row(name=u'name3', title=u'c', fraction=u'3')
=============================================
Row(name=u'name1', title=u'a', fraction=u'1')                                   
Row(name=u'name3', title=u'c', fraction=u'3')
Row(name=u'name4', title=u'd', fraction=None)
=============================================
Row(name=u'name1', title=u'a', fraction=u'1')
Row(name=None, title=None, fraction=u'2')
Row(name=u'name3', title=u'c', fraction=u'3')
=============================================
Row(name=u'name1', title=u'a', fraction=u'1')
Row(name=None, title=None, fraction=u'2')
Row(name=u'name3', title=u'c', fraction=u'3')
Row(name=u'name4', title=u'd', fraction=None)
"""

sc.stop()
