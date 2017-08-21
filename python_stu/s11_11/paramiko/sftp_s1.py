#coding:utf-8
__author__ = 'xuefeng'
import paramiko

transport = paramiko.Transport(('192.168.1.11',22))
transport.connect(username='root',password='123456')

sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put('/tmp/location.py','/tmp/test.py')
sftp.get('/tmp/test.py','/tmp/location2.py')

transport.close()