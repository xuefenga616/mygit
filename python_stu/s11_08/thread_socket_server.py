#coding:utf-8
__author__ = 'xuefeng'
import SocketServer,os

class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        # print self.request,self.client_address,self.server
        conn = self.request
        print "got connection from:",self.client_address

        while True:
            cmd = conn.recv(1024)
            print "Recv from [%s]  cmd:%s" %(self.client_address,cmd)
            cmd_res = os.popen(cmd).read()
            print len(cmd_res)
            conn.send(str(len(cmd_res)))
            conn.recv(1024) #加上此句，隔开上下句，解决粘包
            conn.sendall(cmd_res)

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('192.168.1.17',8000),MyServer)
    server.serve_forever()
