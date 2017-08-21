#coding:utf-8
__author__ = 'Administrator'

# 单例模式：内存中只存在一个实例
class SqlHelper:
    __static_instance = None
    def __init__(self):
        self.hostname = '0.0.0.0'
        self.port = 3306
        self.user = 'root'
        self.pwd = '123456'
    @classmethod
    def instance(cls): #类方法
        # cls = SqlHelper
        if cls.__static_instance:
            return cls.__static_instance
        else:
            cls.__static_instance = SqlHelper()
            return cls.__static_instance
    def fetch(self):
        pass
    def remove(self):
        pass

print id(SqlHelper.instance())
print id(SqlHelper.instance())
print id(SqlHelper.instance())
print id(SqlHelper.instance())
print id(SqlHelper.instance())
print id(SqlHelper.instance())
print id(SqlHelper.instance())

def get_user():
    obj = SqlHelper()
    obj.fetch()
    return "1"

def del_user():
    obj = SqlHelper()
    obj.remove()
