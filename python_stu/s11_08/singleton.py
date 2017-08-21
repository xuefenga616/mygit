#coding:utf-8
__author__ = 'Administrator'

# 单例模式：内存中只存在一个实例
class SqlHelper:
    def __init__(self):
        self.hostname = '0.0.0.0'
        self.port = 3306
        self.user = 'root'
        self.pwd = '123456'
    def fetch(self):
        pass
    def remove(self):
        pass

while True:
    handle_type = raw_input('type:')


obj = SqlHelper()
obj.fetch()
obj.remove()