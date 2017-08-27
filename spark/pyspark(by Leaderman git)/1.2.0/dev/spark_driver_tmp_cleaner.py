import time
import os

clean_endtime = time.time() - (24 * 3600)

print clean_endtime

tmp = "/tmp"

paths = os.listdir(tmp)

for path in paths:
    spark_clean_dir = os.path.join(tmp, path)

    if os.path.isdir(spark_clean_dir) and (path.startswith("spark-") or path.endswith("_resources")) and os.path.getmtime(spark_clean_dir) <= clean_endtime:
       	os.rmdir(spark_clean_dir)
