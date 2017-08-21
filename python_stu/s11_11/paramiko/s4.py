#coding:utf-8
__author__ = 'xuefeng'
import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/home/xuefeng/.ssh/id_rsa')

transport = paramiko.Transport(('192.168.1.11',22))
transport.connect(username='root',pkey=private_key)

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin,stdout,stderr = ssh.exec_command('ls')
print stdout.read()
ssh.close()