#_*_coding:utf-8_*_
'''
Created on 2015��4��10��

@author: Administrator
'''


class BaseService(object):  
    def __init__(self):
        self.name = 'BaseService'
        self.interval = 300
        self.last_time = 0
        self.plugin_name = 'your_plugin_name'
        self.triggers = {}
    


