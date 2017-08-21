#coding:utf-8
__author__ = 'xuefeng'
import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/home/xuefeng/.ssh/id_rsa')

transport = paramiko.Transport(('192.168.1.11',22))
transport.connect(username='root',pkey=private_key)

sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put('/tmp/location.py','/tmp/test.py')
sftp.get('/tmp/test.py','/tmp/location2.py')

transport.close()