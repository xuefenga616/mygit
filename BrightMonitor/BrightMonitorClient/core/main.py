#coding:utf-8
__author__ = 'xuefeng'

import client
import os,sys

class command_handler(object):
    def __init__(self,sys_args):
        self.sys_args = sys_args
        if len(self.sys_args) < 2:
            sys.exit(self.help_msg())
        self.command_allowcator()

    def command_allowcator(self):   #处理输入的参数
        if hasattr(self,self.sys_args[1]):
            func = getattr(self,self.sys_args[1])
            return func()
        else:
            print "command does not exist!"
            self.help_msg()
    def help_msg(self):
        valid_commands = '''
        start   start monitor client
        stop    stop monitor client
        '''
        sys.exit(valid_commands)
    def start(self):
        print "going to start the monitor client"
        Client = client.ClientHandle()
        Client.forever_run()
    def stop(self):
        print "stopping the monitor client"