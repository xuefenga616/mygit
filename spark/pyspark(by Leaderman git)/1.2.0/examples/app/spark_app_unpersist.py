from pyspark import SparkConf, SparkContext, StorageLevel

conf = SparkConf().setAppName("spark_app_unpersist")

sc = SparkContext(conf=conf)

datas = sc.parallelize([1, 2, 3, 4, 5])

datas.persist(StorageLevel.MEMORY_AND_DISK)

datas.unpersist()

sc.stop()
