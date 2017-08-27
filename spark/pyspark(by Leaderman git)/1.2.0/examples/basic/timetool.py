from datetime import datetime, timedelta


def getHDFSHourDir(timeStr):
    return datetime.strptime(timeStr, "%Y%m%d%H%M%S").strftime("%Y_%m_%d/%H/")


def getHDFSDayDir(timeStr):
    return datetime.strptime(timeStr, "%Y%m%d%H%M%S").strftime("%Y_%m_%d/")


def getHDFSPreHourDir(timeStr):
    return (datetime.strptime(timeStr, "%Y%m%d%H%M%S") - timedelta(hours=1)).strftime("%Y_%m_%d/%H/")


def getHDFSPreDayDir(timeStr):
    return (datetime.strptime(timeStr, "%Y%m%d%H%M%S") - timedelta(days=1)).strftime("%Y_%m_%d/")

if __name__ == "__main__":
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    print "now: " + now
    print "getHDFSHourDir:", getHDFSHourDir(now)
    print "getHDFSDayDir:", getHDFSDayDir(now)
    print "getHDFSPreHourDir:", getHDFSPreHourDir(now)
    print "getHDFSPreDayDir:", getHDFSPreDayDir(now)
