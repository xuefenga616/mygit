from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
import MySQLdb

conf = SparkConf().setAppName("sae_nginx_top_url")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

"""
def mysqldb(host, port, user, passwd, db, sql):
    conn = None

    cur = None

    try:
        conn = MySQLdb.connect(host=host, port=port, user=user,
                               passwd=passwd, db=db, charset="utf8")

        cur = conn.cursor()

        cur.execute(sql)

        return cur.fetchall()
    except Exception, e:
        pass
    finally:
        if cur:
            try:
                cur.close()
            except Exception, e:
                pass

        if conn:
            try:
                conn.close()
            except Exception, e:
                pass

top_domain_list = mysqldb("m3353i.apollo.grid.sina.com.cn", 3353, "data_history", "f3u4w8n7b3h", "sae",
                          "select domain from (select domain,round(sum(flow)/1024/1024,0)  as flow_MB     from sae.sae_nginx_flow flow    where DATE_SUB(CURDATE(), INTERVAL 2 DAY) = date group by domain order by flow_MB desc limit 20)A")
"""

top_domain_dict = {u'344.3434dddty.vipsinaapp.com': 12, u'1.appgift.sinaapp.com': 14, u'fansmen.cn': 20, u'lib.sinaapp.com': 2, u'm.miaoche.com': 6, u'www.myhousead.sinaapp.com': 8, u'www.miaoche.com': 5, u'www.ruc.edu.cn': 9, u'better01.sinaapp.com': 19, u'tenyoung.sinaapp.com': 4,
                   u'hg01.zsgjs.com': 17, u'www.neitui.me': 16, u'cn2.php.net': 11, u'app1314.com': 18, u'kjs123.sinaapp.com': 1, u'tracker.sinaapp.com': 3, u'ah.zsgjs.com': 15, u'ku.ent.sina.com.cn': 10, u'www.backgrounds.sinaapp.com': 7, u'liukebin.sinaapp.com': 13}

"""
i = 1

for domain in top_domain_list:
    top_domain_dict[domain[0]] = i

    i = i + 1

print top_domain_dict
"""

jsonRDD = hc.jsonFile(
    "hdfs://dip.cdh5.dev:8020/user/hdfs/rawlog/app_saesinacomkafka12345_nginx/2015_10_22/09")

hc.registerRDDAsTable(jsonRDD, "temp_schema")


def if_in_top_10_domain(domain):
    if domain == '' or domain == None or len(domain) < 3:
        return 'no'
    else:
        if top_domain_dict.has_key(domain):
            return top_domain_dict[domain]
        else:
            return 'no'

hc.registerFunction("temp_if_in_top_10_domain", if_in_top_10_domain)

spark_sql = '''select domain,url,cast(sum(body_bytes_sent) as bigint) as flow from (
                select domain,
                split(request,'\\\\?')[0] as url,
                body_bytes_sent
                from temp_schema
                where body_bytes_sent>0 and temp_if_in_top_10_domain(domain)!='no'
                )A
           group by domain,url limit 100
'''

rows_temp = hc.sql(spark_sql).map(lambda row: (
    (row.domain, if_in_top_10_domain(row.domain), row.url, row.flow), None))


def partitionFunc(key):
    return top_domain_dict[key[0]]


def keyFunc(key):
    return key[3]


def topTenFunc(iter):
    buffer = []

    for pair in iter:
        if len(buffer) >= 10:
            break
        else:
            buffer.append(pair[0])

    return buffer

rows = rows_temp.repartitionAndSortWithinPartitions(
    numPartitions=20, partitionFunc=partitionFunc, ascending=False, keyfunc=keyFunc).mapPartitions(topTenFunc).collect()

for row in rows:
    print row

sc.stop()
