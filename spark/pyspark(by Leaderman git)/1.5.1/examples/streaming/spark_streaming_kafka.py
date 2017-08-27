from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

conf = SparkConf().setAppName(
    "spark_streaming_kafka").setMaster("local[2]")

sc = SparkContext(conf=conf)

streamingCtx = StreamingContext(sc, 10)

datas = KafkaUtils.createStream(
    streamingCtx, "10.13.4.44:2181", "spark_streaming_kafka", {"spark_streaming": 1})

lines = datas.map(lambda data: data[1])

words = lines.flatMap(lambda line: line.split(" "))

wordcounts = words.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)

wordcounts.pprint()

streamingCtx.start()

streamingCtx.awaitTermination()
