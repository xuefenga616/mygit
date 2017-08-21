#coding:utf-8
__author__ = 'xuefeng'
import gevent
import urllib2

def f(url):
    print "GET: %s" %url
    resp = urllib2.urlopen(url)
    data = resp.read()
    print "%d bytes received from %s." %(len(data),url)

gevent.joinall([
    gevent.spawn(f,'https://www.python.org/'),
    gevent.spawn(f,'http://www.baidu.com/'),
    gevent.spawn(f,'https://github.com/'),
])
