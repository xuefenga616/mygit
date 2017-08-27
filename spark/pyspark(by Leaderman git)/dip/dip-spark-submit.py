import sys
import os
import commands

if len(sys.argv) == 1:
    print "dip-spark-submit.py version hadoopConfDir sparkConfDir sparkParams"

    exit()

version = sys.argv[1]

home = ""

versions = ["1.5.1"]

if version in versions:
    if version == "1.5.1":
        home = "/usr/lib/spark-1.5.1-bin-2.5.0-cdh5.3.2"
else:
    print "version must be [" + ",".join(versions) + "]"

    exit()

hadoopConf = sys.argv[2]

if os.path.exists(hadoopConf):
    files = os.listdir(hadoopConf)

    if not ("core-site.xml" in files and "hdfs-site.xml" in files and "mapred-site.xml" in files and "yarn-site.xml" in files):
        print hadoopConf + " must have files: core-site.xml hdfs-site.xml mapred-site.xml yarn-site.xml"

        exit()
else:
    print hadoopConf + " not exists"

    exit()

sparkConf = sys.argv[3]

if os.path.exists(sparkConf):
    files = os.listdir(sparkConf)

    if not ("spark-env.sh" in files and "spark-defaults.conf" in files):
        print sparkConf + " must have files: spark-env.sh spark-defaults.conf"

        exit()
else:
    print sparkConf + " not exists"

    exit()

offline = "offline"
online = "online"

if not ((offline in hadoopConf and online in sparkConf) or (online in hadoopConf and online in sparkConf)):
    print "hadoopConf and sparkConf must have the same mode: offline or online"

    exit()

cmd = "export HADOOP_CONF_DIR=%s;" % hadoopConf

cmd += "export SPARK_CONF_DIR=%s;" % sparkConf

cmd += "export PYTHONHASHSEED=0;"

cmd += ("%s/bin/spark-class org.apache.spark.deploy.SparkSubmit " %
        home + " ".join(sys.argv[4:]))

output = commands.getoutput(cmd)

print output
