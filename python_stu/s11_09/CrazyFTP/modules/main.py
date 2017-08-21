#coding:utf-8
__author__ = 'xuefeng'
import os,sys
import socket_server
from conf import settings

class ArgvHandler(object):
    def __init__(self,args):
        self.args = args
        self.argv_parser()
    def argv_parser(self):
        if len(self.args) == 0:
            self.help_msg()
        else:
            if hasattr(self,self.args[0]):
                func = getattr(self,self.args[0])
                func()
            else:
                self.help_msg()
    def help_msg(self):
        msg = '''
        start:          start ftp server
        stop:           stop ftp server
        create_account: create ftp user account
        help:           print help msg
        '''
        sys.exit(msg)
    def start(self):
        t = socket_server.SocketServer.ThreadingTCPServer((settings.BIND_HOST,settings.BIND_PORT),socket_server.FtpServer) #创建socket server
        t.serve_forever()   #启动socket server
    def stop(self):
        print "lalala"