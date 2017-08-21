#coding:utf-8
__author__ = 'xuefeng'
import paramiko
import uuid

class Haproxy(object):
    def __init__(self):
        self.host = "192.168.1.11"
        self.port = 22
        self.username = "root"
        self.private_key = paramiko.RSAKey.from_private_key_file('/home/xuefeng/.ssh/id_rsa')

    def create_file(self):
        file_name = str(uuid.uuid4())
        with open(file_name,'w') as f:
            f.write('hahaha')
        return file_name

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,pkey=self.private_key)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run(self):
        #连接
        self.connect()
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        sftp = paramiko.SFTPClient.from_transport(self.__transport)

        filename = self.create_file()
        self.upload()
        self.rename()
        #关闭
        self.close()

    def upload(self):
        pass

    def rename(self):
        pass

if __name__ == '__main__':
    ha = Haproxy()
    ha.run()
