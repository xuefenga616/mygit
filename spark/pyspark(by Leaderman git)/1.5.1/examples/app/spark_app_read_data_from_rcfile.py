from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_read_data_from_rcfile")

sc = SparkContext(conf=conf)

rowRDD = sc.hadoopFile(path="hdfs://dip.cdh5.dev:8020/user/yurun/rcfile",
                       inputFormatClass="org.apache.hadoop.hive.ql.io.RCFileInputFormat",
                       keyClass="org.apache.hadoop.io.LongWritable",
                       valueClass="org.apache.hadoop.hive.serde2.columnar.BytesRefArrayWritable",
                       valueConverter="com.sina.dip.spark.converter.BytesRefArrayWritableToObjectArrayConverter")

pairs = rowRDD.collect()

for pair in pairs:
    print pair[0], pair[1]

sc.stop()
