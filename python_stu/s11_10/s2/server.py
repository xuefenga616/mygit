#coding:utf-8
__author__ = 'xuefeng'
import select
import socket,time
import Queue

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('192.168.1.17',8080))
s.listen(5)
s.setblocking(False)    #本来默认是阻塞，这里设置为不阻塞

inputs = [s,]     #输入的列表写成动态的，client发来的数据到后面去append
output = []
message = {}        # {'c1':队列1, 'c2':队列2}
while True:
    rList,wList,e = select.select(inputs,output,inputs,0.2)

    #读写拆分:
    #文件描述符可读,rList感知（变化才感知）
    #文件描述符可写,wList感知（连接就感知）
    for r in rList:     #如果是空列表，for循环不会执行
        if r == s:      #如果是服务端，监听服务端的端口
            conn,address = r.accept()   #conn是客户端句柄
            inputs.append(conn)         #把客户端发来的数据追加到inputs的输入中
            message[conn] = Queue.Queue()     #创建一个队列
        else:           #即r == conn，监听客户端的端口
            client_data = r.recv(1024)
            if client_data:
                #获取数据
                output.append(r)
                #在指定队列中插入数据
                message[r].put(client_data)
            else:       #客户端断开连接时，会发送来一条空消息
                inputs.remove(r)    #移除客户端句柄

    for w in wList:
        #去指定队列取数据
        try:
            data = message[w].get_nowait()  #不阻塞取消息
            w.sendall(data.upper())         #发完了，下面移除
        except Queue.Empty:
            pass            #出了异常，不需要写了，下面移除
        output.remove(w)    #移除
        del message[w]



