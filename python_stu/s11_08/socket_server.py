#coding:utf-8
__author__ = 'Administrator'
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('192.168.1.101',8080))
sock.listen(5)      #最大等待连接数
while True:
    conn,addr = sock.accept()
    client_data = conn.recv(1024)     #最多接收1024
    print client_data
    conn.send('do not answer')
    conn.close()
