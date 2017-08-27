from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

conf = SparkConf().setAppName(
    "spark_streaming_wordcount").setMaster("local[2]")

sc = SparkContext(conf=conf)

streamingCtx = StreamingContext(sc, 1)

StreamingContext()

lines = streamingCtx.socketTextStream("localhost", 9999)

words = lines.flatMap(lambda line: line.split(" "))

pairs = words.map(lambda word: (word, 1))

wordcounts = pairs.reduceByKey(lambda x, y: x + y)

wordcounts.pprint()

streamingCtx.start()

streamingCtx.awaitTermination()
