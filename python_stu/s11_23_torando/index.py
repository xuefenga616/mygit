#coding:utf-8
__author__ = 'xuefeng'
import tornado.ioloop
import tornado.web
from session_demo import Session

#initialize在get、post处理请求之前执行
class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        # my_session['k1']访问 __getitem__ 方法
        self.my_session = Session(self)

class MainHandler(BaseHandler):
    def get(self):
        ret = self.my_session['is_login']
        if ret:
            self.write('index')
        else:
            self.redirect('/login')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('pwd')
        if username == 'alex' and password == '123456':
            self.my_session['is_login'] = 'true'

            self.redirect('/index')
        else:
            self.render('login.html')

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',

}

application = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/login", LoginHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()