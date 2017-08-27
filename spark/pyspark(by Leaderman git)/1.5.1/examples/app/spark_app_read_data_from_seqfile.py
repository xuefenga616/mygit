from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("spark_app_read_data_from_seqfile")

sc = SparkContext(conf=conf)

lineRDD = sc.hadoopFile(path="hdfs://dip.cdh5.dev:8020/user/yurun/seqfile",
                        inputFormatClass="org.apache.hadoop.mapred.SequenceFileInputFormat",
                        keyClass="com.sina.dip.spark.converter.IntArrayWritable",
                        valueClass="org.apache.hadoop.io.NullWritable",
                        keyConverter="com.sina.dip.spark.converter.IntArrayWritableToObjectArrayConverter").map(lambda pair: pair[0])

lines = lineRDD.collect()

for line in lines:
    print line

sc.stop()
