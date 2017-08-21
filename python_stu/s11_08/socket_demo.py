#coding:utf-8
__author__ = 'Administrator'
import socket

def handle_request(client):
    buf = client.recv(1024)
    print buf
    client.send("HTTP/1.1 200 OK\r\n\r\n")  #HTTP的请求头
    client.send("Hello,World")

def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #创建socket对象
    sock.bind(('192.168.1.101',8080))             #监听端口
    sock.listen(5)                          #开始监听

    while True:
        connection,address = sock.accept()  #connection代表客户端socket对象，address是客户端地址
        handle_request(connection)
        connection.close()

if __name__ == "__main__":
    main()