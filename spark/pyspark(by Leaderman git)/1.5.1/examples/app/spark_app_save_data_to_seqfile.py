from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_save_data_to_seqfile")

sc = SparkContext(conf=conf)

arrays = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

pairRDD = sc.parallelize(arrays).map(lambda array: (array, None))

pairRDD.saveAsHadoopFile(path="hdfs://dip.cdh5.dev:8020/user/yurun/seqfile",
                         outputFormatClass="org.apache.hadoop.mapred.SequenceFileOutputFormat",
                         keyClass="com.sina.dip.spark.converter.IntArrayWritable",
                         valueClass="org.apache.hadoop.io.NullWritable",
                         keyConverter="com.sina.dip.spark.converter.ObjectArrayToIntArrayWritableConverter"
                         )

sc.stop()
