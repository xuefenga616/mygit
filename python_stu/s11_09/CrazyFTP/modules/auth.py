#coding:utf-8
__author__ = 'xuefeng'
from conf import settings
import json,sys

def authentication(user,passwd):
    engine_obj = fetch_account()
    return engine_obj.auth(user,passwd)

def fetch_account():
    acc_storage = settings.ACCOUNT_DB.get("engine")     #存储的方法
    if hasattr(sys.modules[__name__], "engine_"+acc_storage):  #没有类，直接在模块下取方法(也可以反射类)
        obj = getattr(sys.modules[__name__], "engine_"+acc_storage) #反射类
        #obj = getattr(__import__, "engine_"+acc_storage)   #反射函数
        return obj()

class engine_file(object):
    def __init__(self):
        print "calling engine..."
    def auth(self,user,passwd):
        print "----engine file----"
        filename = settings.ACCOUNT_DB.get("name")
        assert filename is not None     #断言
        with file(filename,'rb') as f:
            acc_dic = json.load(f)
            user_in_db = acc_dic.get(user)
            if user_in_db:
                if passwd == user_in_db.get("password"):
                    #user authentication success
                    msg = "pass authentication"
                    status = True
                else:
                    msg = "wrong username or password"
                    status = False
            else:
                msg = "no such user"
                status = False
        return status,msg
