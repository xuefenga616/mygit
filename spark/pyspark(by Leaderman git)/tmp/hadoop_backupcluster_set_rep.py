import commands
import re
import datetime
import sys

now = datetime.datetime.now().strftime("%Y%m%d")

pathPattern = re.compile(".*(/backup/day/mysql.*)")
datePattern = re.compile(".*/backup/day/mysql.*/(\d{8})")

output = commands.getoutput("hadoop fs -ls /backup/day/*/")

hdfsDirs = output.split("\n")

paths = []

for hdfsDir in hdfsDirs:
    pathMatcher = pathPattern.match(hdfsDir)
    dateMatcher = datePattern.match(hdfsDir)

    if pathMatcher and dateMatcher:
        date = dateMatcher.group(1)

        if date < now:
            paths.append(pathMatcher.group(1))

for path in paths:
    command = "hadoop fs -setrep -R " + sys.argv[1] + " " + path

    print commands.getoutput(command)
