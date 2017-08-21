#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from hashlib import sha1
import os, time

from ha import HashRing

session_container = {}

create_session_id = lambda: sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()

class Session(object):

    session_id = "__sessionId__"

    def __init__(self, request):
        session_value = request.get_cookie(Session.session_id)
        if not session_value:
            self._id = create_session_id()
        else:
            self._id = session_value
        request.set_cookie(Session.session_id, self._id)

    def __getitem__(self, key):
        # 根据 self._id ，在一致性哈西中找到其对应的服务器IP
        # 找到相对应的redis服务器，如： r = redis.StrictRedis(host='localhost', port=6379, db=0)
        # 使用python redis api 链接
        # 获取数据，即：
        # return self._redis.hget(self._id, name)
        pass

    def __setitem__(self, key, value):
        # 根据 self._id ，在一致性哈西中找到其对应的服务器IP
        # 使用python redis api 链接
        # 设置session
        # self._redis.hset(self._id, name, value)
        pass


    def __delitem__(self, key):
        # 根据 self._id 找到相对应的redis服务器
        # 使用python redis api 链接
        # 删除，即：
        # return self._redis.hdel(self._id, name)
        pass


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        # my_session['k1']访问 __getitem__ 方法
        self.my_session = Session(self)


class MainHandler(BaseHandler):

    def get(self):
        print self.my_session['c_user']
        print self.my_session['c_card']
        self.write('index')

class LoginHandler(BaseHandler):

    def get(self):
        self.write("OK")

    def post(self, *args, **kwargs):

        username = self.get_argument('name')
        password = self.get_argument('pwd')
        if username == 'alex' and password == '123456':

            self.my_session['c_user'] = 'alex'
            self.my_session['c_card'] = '123456'

            self.redirect('/index')
        else:
            self.render('login.html', **{'status': '用户名或密码错误'})

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': 'aiuasdhflashjdfoiuashdfiuh',
    'login_url': '/login'
}

application = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/login", LoginHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
