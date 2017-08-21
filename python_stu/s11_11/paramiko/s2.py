#coding:utf-8
__author__ = 'xuefeng'
import paramiko

transport = paramiko.Transport(('192.168.1.11',22))
transport.connect(username='root',password='123456')

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin,stdout,stderr = ssh.exec_command('ls')
print stdout.read()

transport.close()