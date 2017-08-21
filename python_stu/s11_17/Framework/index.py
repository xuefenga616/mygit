#!/usr/bin/env python
#coding:utf-8
from wsgiref.simple_server import make_server
from url import urlpatterns


def RunServer(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    url = environ['PATH_INFO']
    print url
    func = None
    for item in urlpatterns:
        if item[0] == url:
            func = item[1]
            break
    if func:
        return func()
    else:
        return '404 not found'

if __name__ == '__main__':
    httpd = make_server('', 8000, RunServer)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()
