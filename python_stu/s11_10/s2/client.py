#coding:utf-8
__author__ = 'xuefeng'

import socket

s = socket.socket()
s.connect(('192.168.1.17',8080))
s.settimeout(5)

while True:
    inp = raw_input("please input:")
    s.sendall(inp)
    print s.recv(1024)


s.close()
