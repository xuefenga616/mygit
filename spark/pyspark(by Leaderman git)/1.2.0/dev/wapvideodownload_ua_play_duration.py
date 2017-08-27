from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from decimal import Decimal
from datetime import datetime, date
from pyspark.sql import StructType, StructField, ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType, StringType, BooleanType, TimestampType, DateType, ArrayType, MapType

conf = SparkConf().setAppName("spark_sql_datatype")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

spark_sql = '''select '%s' as job_date,ua,version,video_network,video_is_autoplay,
             video_play_duration_group,video_duration_group,play_process_group,
             sum(num) as num
             from datacubic.app_picserversweibof6vwt_wapvideodownload
             where log_dir>='%s' and log_dir<='%s' and version>='5.4.5'
             and play_process_group!='NoPlay' and play_process_group!='-'
             group by ua,version,video_network,video_is_autoplay,
             video_play_duration_group,video_duration_group,play_process_group''' % ("20151027150000", "20151027150000", "20151027150000")

#rows = hc.sql("select count(distinct(video_duration_group)) from datacubic.app_picserversweibof6vwt_wapvideodownload where log_dir = 20151027150000").collect()

rows = hc.sql(spark_sql).collect()

sc.stop()

for row in rows:
    print row
