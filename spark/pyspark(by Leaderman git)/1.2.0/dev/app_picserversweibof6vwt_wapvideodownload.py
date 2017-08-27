# coding: utf-8

from pyspark import SparkConf
from dip.spark import SparkContext
from pyspark.sql import HiveContext
from dip.util import timetool
import sys
import random

reload(sys)
sys.setdefaultencoding("utf-8")

import re
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType
import json
import time

conf = SparkConf().setAppName(
    "app_picserversweibof6vwt_wapvideodownload_to_hdfs")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

try:
    source = sc.textFile(
        "/user/hdfs/rawlog/app_picserversweibof6vwt_wapvideodownload/" + timetool.getHDFSDayDir(sys.argv[1]))

    pattern = re.compile("^([^`]*)`([^`]*)")

    def lineParse(line):
        matcher = pattern.match(line)

        if not matcher:
            return None

        videodownload_info = matcher.group(1)

        try:
            jsonObj = json.loads(videodownload_info)

            if "ua" not in jsonObj:
                return None

            ua = jsonObj["ua"]

            if len(ua.split("__")) < 3:
                return None

            version = ua.split("__")[2]

            if version >= "5.4.0":
                __date = str(jsonObj["__date"]) if "__date" in jsonObj else ""

                video_mediaid = jsonObj[
                    "video_mediaid"] if "video_mediaid" in jsonObj else ""

                video_url = jsonObj[
                    "video_url"] if "video_url" in jsonObj else ""

                video_cdn = jsonObj[
                    "video_cdn"] if "video_cdn" in jsonObj else ""

                video_network = jsonObj[
                    "video_network"] if "video_network" in jsonObj else ""

                ip = jsonObj["ip"] if "ip" in jsonObj else ""

                video_play_type = str(jsonObj[
                    "video_play_type"]) if "video_play_type" in jsonObj else ""

                video_play_type_duration = str(jsonObj[
                    "video_play_type_duration"]) if "video_play_type_duration" in jsonObj else ""

                video_error_code = str(jsonObj[
                    "video_error_code"]) if "video_error_code" in jsonObj else ""

                video_error_msg = jsonObj[
                    "video_error_msg"] if "video_error_msg" in jsonObj else ""

                buffer_duration_list = []

                if "buffer_duration_list" in jsonObj:
                    for v in jsonObj["buffer_duration_list"]:
                        buffer_duration_list.append(int(v))

                video_duration = str(jsonObj[
                    "video_duration"]) if "video_duration" in jsonObj else ""

                video_play_duration = str(jsonObj[
                    "video_play_duration"]) if "video_play_duration" in jsonObj else ""

                if version == "5.4.0":
                    __date = __date[0:10]

                    if "video_buffer_type" not in jsonObj:
                        video_play_type = ""
                    else:
                        if jsonObj["video_buffer_type"] != "1":
                            video_play_type = str(jsonObj["video_buffer_type"])

                    if "video_buffer_type" not in jsonObj or "video_buffer_duration" not in jsonObj:
                        video_play_type_duration = ""
                    else:
                        if jsonObj["video_buffer_type"] != "1":
                            video_play_type_duration = str(jsonObj[
                                "video_buffer_duration"])

                    if "video_buffer_type" in jsonObj and jsonObj["video_buffer_type"] == 1 and "video_buffer_duration" in jsonObj:
                        buffer_duration_list = [
                            int(jsonObj["video_buffer_duration"])]
                else:
                    __date = str(jsonObj[
                        "video_log_time"]) if "video_log_time" in jsonObj else ""

                    __date = __date[0:10]

                    if "video_time_duration" not in jsonObj:
                        video_play_type = ""
                    else:
                        for v in jsonObj["video_time_duration"]:
                            if "type" in v and v["type"] != "1":
                                video_play_type = str(v["type"])

                                break

                    if "video_time_duration" in jsonObj:
                        for v in jsonObj["video_time_duration"]:
                            if "type" in v and "type" != "1" and "duration" in v:
                                video_play_type_duration = str(v["duration"])

                                break

                    if "video_error_info" in jsonObj and "error_code" in jsonObj["video_error_info"]:
                        video_error_code = str(jsonObj[
                            "video_error_info"]["error_code"])

                    if "video_error_info" in jsonObj and "error_msg" in jsonObj["video_error_info"]:
                        video_error_msg = str(jsonObj[
                            "video_error_info"]["error_msg"])

                    if "video_time_duration" in jsonObj:
                        for v in jsonObj["video_time_duration"]:
                            if "type" in v and v["type"] == "1" and "duration" in v:
                                buffer_duration_list.append(int(v["duration"]))
            else:
                return None

            return (__date, video_mediaid, video_url, ua, video_cdn, video_network, ip, video_play_type,
                    video_play_type_duration, video_error_code, video_error_msg, buffer_duration_list, video_duration, video_play_duration)

        except Exception, e:
            pass

        return None

    rows = source.map(lineParse).filter(lambda columns: columns)

    schema = StructType([StructField("cdate", StringType(), False), StructField(
        "video_mediaid", StringType(), False), StructField("video_url", StringType(), False), StructField("ua", StringType(), False), StructField("video_cdn", StringType(), False), StructField("video_network", StringType(), False), StructField("ip", StringType(), False), StructField("video_play_type", StringType(), False), StructField("video_play_type_duration", StringType(), False), StructField("video_error_code", StringType(), False), StructField("video_error_msg", StringType(), False), StructField("buffer_duration_list", ArrayType(IntegerType(), False), False), StructField("video_duration", StringType(), False), StructField("video_play_duration", StringType(), False)])

    table = hc.applySchema(rows, schema)

    table.registerTempTable("temp_table")

    def parseCDN(video_cdn):
        if not video_cdn:
            return ""

        words = video_cdn.split("s=")

        if len(words) >= 2:
            return words[1].split(",")[0]

        return ""

    hc.registerFunction("parseCDN", parseCDN)

    def cal_buffer_num(set):
        buffer_count = 0
        buffer_t_sum = 0
        buffer_smaller_500ms_count = 0
        buffer_bigger_2min_count = 0

        if set == None:
            pass
        else:
            list = set

            for s in list:
                if s >= 500 and s <= 120000:
                    buffer_count = buffer_count + 1
                    buffer_t_sum = buffer_t_sum + s
                elif s < 500:
                    buffer_smaller_500ms_count = buffer_smaller_500ms_count + 1
                elif s > 120000:
                    buffer_bigger_2min_count = buffer_bigger_2min_count + 1

        return (buffer_count, buffer_t_sum, buffer_smaller_500ms_count, buffer_bigger_2min_count)

    hc.registerFunction("cal_buffer_num", cal_buffer_num, StructType([StructField("buffer_count", IntegerType()), StructField(
        "buffer_t_sum", IntegerType()), StructField("buffer_smaller_500ms_count", IntegerType()), StructField("buffer_bigger_2min_count", IntegerType())]))

    result = hc.sql("""
    select 
            from_unixtime(cast(round(cdate,0) as bigint),'yyyy-MM-dd') as date,
            (case when func.ipToLocationBySina(ip)[0]='中国' then func.ipToLocationBySina(ip)[1]
                  when func.ipToLocationBySina(ip)[0]!='中国' then func.ipToLocationBySina(ip)[0]
                  end) as province,
            func.ipToLocationBySina(ip)[4] as isp,
            (case when video_cdn like 'f=cnct%' then 'cnct'
                  when video_cdn like 'f=alicdn%' then 'ali'
                  when video_cdn like 'f=edge%' then 'edge'
                  else 'else' END) as cdn,
            parseCDN(video_cdn) as idc,
            (CASE WHEN upper(ua) LIKE '%IPHONE%' THEN 'IPHONE'
                  WHEN upper(ua) LIKE '%ANDROID%' THEN 'ANDROID'
                  ELSE '-' END) AS ua,
            split(ua, '__')[2] as version,
            video_network,
            video_error_code,
            video_error_msg,
            video_play_type,
            video_play_duration,
            video_duration,
            (case
            when video_play_duration>0 and video_duration>0 then cast(round(video_play_duration/video_duration,1) as VARCHAR(5))
            when video_play_duration='' or video_play_duration=0 or video_play_duration='None' then 'NoPlay'
            else '-' END) as play_process_group,
            (case
            when video_duration>0 then int(video_play_duration/video_duration)
            else 0
            END)  as play_process,
            video_play_type_duration,
            (case when video_play_type_duration <=2000 then '<=2000ms'
                  when video_play_type_duration>2000 then '>2000ms' else '-' end )as init_timetag,
            cal_buffer_num(buffer_duration_list) as cal_buffer_num from temp_table where (video_url like '%%us.sina%' or video_mediaid like '1034:%') and split(ua, '__')[2] >='5.4'
    """)

    result.registerTempTable("temp_table2")

    def convertNoneToZero(columns):
        convert = list(columns)

        if not convert[14]:
            convert[14] = 0

        if not convert[15]:
            convert[15] = 0

        if not convert[16]:
            convert[16] = 0

        if not convert[17]:
            convert[17] = 0

        if not convert[18]:
            convert[18] = 0

        return tuple(convert)

    preDay = 1
    preDate = time.localtime(
        time.mktime(time.strptime(sys.argv[1], "%Y%m%d%H%M%S")) - preDay * 24 * 60 * 60)
    job_date = time.strftime("%Y-%m-%d", preDate)

    result = hc.sql("select '" + job_date + "' as job_date," + """date,province,isp,cdn,idc,ua,version,video_network, video_error_code,video_error_msg,video_play_type,
            init_timetag,cal_buffer_num.buffer_count,cal_buffer_num.buffer_smaller_500ms_count,cal_buffer_num.buffer_bigger_2min_count,
            play_process_group,
            sum(video_play_type_duration) as sum_video_play_type_duration,sum(cal_buffer_num.buffer_t_sum) as sum_buffer_t_sum,
            sum(video_play_duration) as sum_video_play_duration,sum(video_duration) as sum_video_duration,
            sum(play_process) as sum_play_process,
            count(1)as num,
            '' as temp_20,'' as temp_21,'' as temp_22,'' as temp_23,'' as temp_24,'' as temp_25
            from temp_table2
            group by date,province,isp,cdn,idc,ua,version,video_network, video_error_code,video_error_msg,video_play_type,
            init_timetag,cal_buffer_num.buffer_count,cal_buffer_num.buffer_smaller_500ms_count,cal_buffer_num.buffer_bigger_2min_count,
            play_process_group
    """).map(convertNoneToZero)

    """
    hive_dip = 'datacubic'
    hive_table = 'app_picserversweibof6vwt_wapvideodownload_yurun_test'
    hive_partition = time.strftime(
        "%Y%m%d", time.strptime(sys.argv[1], "%Y%m%d%H%M%S")) + '000000'
    props = {"db": hive_dip, "table": hive_table,
             "partition": hive_partition, "overwrite": True}
    sc.saveRDDToHive(result, props)

    lambda row: isinstance(row, tuple))
    """

    def tupleToStrs(tuple):
        strs = []

        for e in tuple:
            if isinstance(e, str):
                strs.append(e)
            elif isinstance(e, unicode):
                strs.append(e)
            else:
                strs.append(str(e))

        return "\t".join(strs)

    strRDD = result.map(tupleToStrs)

    kvRDD = strRDD.map(lambda row: (random.randint(1, 10), row))

    hadoopConf = {"mapreduce.output.fileoutputformat.outputdir": "/user/yurun/tmp/1/", "mapred.output.format.class": "org.apache.hadoop.mapred.TextOutputFormat",
                  "mapred.output.key.class": "org.apache.hadoop.io.LongWritable", "mapred.output.value.class": "org.apache.hadoop.io.Text"}

    kvRDD.saveAsHadoopDataset(conf=hadoopConf)
except Exception, e:
    raise
finally:
    sc.stop()
