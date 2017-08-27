from httplib import HTTPConnection
import json


class PyWebHDFS(object):

    __GET = "GET"

    def __init__(self, hostAndPorts, timeout):
        self.hostAndPorts = hostAndPorts

        self.timeout = timeout

    def __getConn(self):
        for hostAndPort in self.hostAndPorts:
            words = hostAndPort.split(":")

            self.conn = HTTPConnection(
                host=words[0], port=int(words[1]), timeout=self.timeout)

            break

        if not self.conn:
            raise RuntimeError("HTTPConnection is null")

    def getFileStatus(self, path):
        self.__getConn()

        self.conn.request(self.__GET, "/webhdfs/v1/user?op=GETFILESTATUS")

        response = self.conn.getresponse()

        if response.status == 200:
        	print response.read()

    def listStatus(self, path, type=None):
        self.__getConn()

        self.conn.request(self.__GET, "/webhdfs/v1/?op=LISTSTATUS")

        response = self.conn.getresponse()

        if response.status == 200:
            result = json.loads(response.read())

            if result and result["FileStatuses"] and result["FileStatuses"]["FileStatus"]:
                return filter(lambda status: True if not type else status["type"] == type, result["FileStatuses"]["FileStatus"])


if __name__ == '__main__':
    hostAndPorts = ["10.210.136.61:50070"]

    timeout = 3

    webhdfs = PyWebHDFS(hostAndPorts, timeout)

    print webhdfs.getFileStatus("/")

    #print webhdfs.listStatus("/", "DIRECTORY")
