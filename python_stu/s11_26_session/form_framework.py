#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from hashlib import sha1
import os, time
import re

class IPFiled(object):
    regular = "^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$"
    def __init__(self,error_msg_dict=None,required=True):
        error_msg = {}  #{'required':'IP不能为空', 'valid':'IP格式错误'}
        if error_msg_dict:
            error_msg.update(error_msg_dict)
        self.required = required
        self.error_msg = error_msg
    def check_valid(self,request_ins,k):
        flag = True
        if self.required:      #需要验证
            if not request_ins.get_argument(k):     #前端输入为空
                flag = False
                print self.error_msg['required']
            else:
                if re.match(self.regular,request_ins.get_argument(k)): #验证成功
                    pass
                else:
                    flag = False
                    print self.error_msg['valid']
        else:
            pass
        return flag

class FileFiled(object):
    pass

class BaseForm(object):
    def is_valid(self,request_ins):
        flag = True
        for k,v in self.__dict__.items():   # __dict__是取出对象的所有元素
            print k,v,request_ins.get_argument(k)
            # v IPField对象
            ret = v.check_valid(request_ins,k)
            if not ret:
                flag = False
        return flag

class Form(BaseForm):
    def __init__(self):
        # self.host = "(.*)"
        # self.port = '(\d+)'
        # self.phone = '^1[3|4|5|8][0-9]\d{8}$'
        self.ip = IPFiled(error_msg_dict={'required':'IP不能为空', 'valid':'IP格式错误'})


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self, *args, **kwargs):
        obj = Form()
        flag = obj.is_valid(self)

        if flag:
            self.write('ok')
        else:
            self.write('error')
        # obj = MainForm()
        # result = obj.check_valid(self)




settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': 'aiuasdhflashjdfoiuashdfiuh',
    'login_url': '/login'
}

application = tornado.web.Application([
    (r"/index", MainHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()