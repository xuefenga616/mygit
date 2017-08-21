#coding:utf-8
__author__ = 'xuefeng'
import select
import socket,time


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('192.168.1.17',8080))
s.listen(5)
s.setblocking(False)    #本来默认是阻塞，这里设置为不阻塞

inputs = [s,]     #输入的列表写成动态的，client发来的数据到后面去append
output = []
while True:
    rList,w,e = select.select(inputs,output,inputs,0.2)
    time.sleep(1)
    print inputs
    #print w

    for r in rList:     #如果是空列表，for循环不会执行
        if r == s:      #如果是服务端，监听服务端的端口
            conn,address = r.accept()   #conn是客户端句柄
            inputs.append(conn)         #把客户端发来的数据追加到inputs的输入中
            output.append(conn)
        else:           #即r == conn，监听客户端的端口
            client_data = r.recv(1024)
            if client_data:
                r.sendall(client_data.upper())
            else:       #客户端断开连接时，会发送来一条空消息
                inputs.remove(r)    #移除客户端句柄


