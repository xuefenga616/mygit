# -*- coding:utf-8 -*-

import socket

sk = socket.socket()
sk.connect(('192.168.1.17',8000))
sk.settimeout(5)

while True:
    inp = raw_input("please input:")
    sk.sendall(inp)
    res_size = int(sk.recv(1024))
    sk.sendall("hahaha")    #防止粘包
    print "going to recv data size:",res_size

    data = ""
    if res_size > 1024:
        data += sk.recv(1024)
        res_size -= 1024
    else:
        data += sk.recv(res_size)
    print data


sk.close()
