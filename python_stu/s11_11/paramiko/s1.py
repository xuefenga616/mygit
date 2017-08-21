#coding:utf-8
__author__ = 'xuefeng'
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   #允许连接不在know_hosts文件中的主机
ssh.connect(hostname='192.168.1.11',port=22,username='root',password='123456',timeout=10)

stdin,stdout,stderr = ssh.exec_command('ls')
print stdout.read()
ssh.close()