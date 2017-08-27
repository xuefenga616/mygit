from pyspark import SparkConf, SparkContext, StorageLevel

conf = SparkConf().setAppName("spark_app_persist")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3, 4, 5])

datas.persist(StorageLevel.MEMORY_AND_DISK)

level = datas.getStorageLevel()

sc.stop()

# Disk Memory Deserialized 1x Replicated
print level
