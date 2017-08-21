#coding:utf-8
__author__ = 'xuefeng'
import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/home/xuefeng/.ssh/id_rsa')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.1.11',port=22,username='root',pkey=private_key,timeout=10)

stdin,stdout,stderr = ssh.exec_command('ls')
print stdout.read()
ssh.close()