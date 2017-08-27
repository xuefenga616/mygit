from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_save_data_to_rcfile")

sc = SparkContext(conf=conf)

rows = [("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9")]

pairRDD = sc.parallelize(rows, 1).map(lambda row: (None, row))

conf = {"hive.io.rcfile.column.number.conf": "3"}

pairRDD.saveAsHadoopFile(path="hdfs://dip.cdh5.dev:8020/user/yurun/rcfile",
                         outputFormatClass="com.sina.dip.spark.output.DipRCFileOutputFormat",
                         keyClass="org.apache.hadoop.io.NullWritable",
                         valueClass="org.apache.hadoop.hive.serde2.columnar.BytesRefArrayWritable",
                         valueConverter="com.sina.dip.spark.converter.ObjectArrayToBytesRefArrayWritableConverter", conf=conf)

sc.stop()
