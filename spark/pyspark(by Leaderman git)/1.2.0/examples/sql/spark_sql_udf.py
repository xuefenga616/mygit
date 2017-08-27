from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, StructType, StructField, StringType, IntegerType, ArrayType, FloatType, MapType

conf = SparkConf().setAppName("spark_sql_udf")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

source = sc.parallelize([("value",)])

schema = StructType([StructField("col", StringType(), False)])

table = hc.applySchema(source, schema)

table.registerTempTable("temp_table")


def func_string():
    return "abc"

hc.registerFunction("func_string", func_string)

rows = hc.sql("select func_string() from temp_table").collect()


def func_int():
    return 123

hc.registerFunction("func_int", func_int, IntegerType())

rows = hc.sql("select func_int() from temp_table").collect()


def func_array():
    # list or tuple
    return [1, 2, 3]

hc.registerFunction("func_array", func_array, ArrayType(IntegerType()))

rows = hc.sql(
    "select val[0], val[1], val[2] from (select func_array() as val from temp_table) t").collect()


def func_struct():
    # tuple
    return (1, 2.0, "3")

hc.registerFunction("func_struct", func_struct, StructType([StructField(
    "first", IntegerType()), StructField("second", FloatType()), StructField("third", StringType())]))

rows = hc.sql(
    "select val.first, val.second, val.third from (select func_struct() as val from temp_table) t").collect()


def func_map():
    # dict
    map = {}

    map["first"] = 1
    map["second"] = 2
    map["third"] = 3

    return map

hc.registerFunction(
    "func_map", func_map, MapType(StringType(), IntegerType()))

rows = hc.sql(
    "select val['first'], val['second'], val['third'] from (select func_map() as val from temp_table) t").collect()

sc.stop()

for row in rows:
    print row
