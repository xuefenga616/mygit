#coding:utf-8
__author__ = 'xuefeng'
import os,sys

basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)
sys.path.append('%s/BrightMonitor' %basedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'BrightMonitor.settings'
import django
django.setup()

from BrightMonitor import settings
import redis

class RedisHelper:
    def __init__(self):
        self.__conn = redis.Redis(host=settings.REDIS_CONN['HOST'],port=6379,db=0,password=settings.REDIS_CONN['PASSWD'])
        self.chan_sub = 'fm104.5'
        self.chan_pub = 'fm104.5'
    def get(self,key):
        return self.__conn.get(key)
    def set(self,key,value):
        return self.__conn.set(key,value)
    def public(self,msg):
        self.__conn.publish(self.chan_pub,msg)
        return True
    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
    def lrange(self,key,start,end):
        return self.__conn.lrange(key,start,end)
    def keys(self,pattern):
        return self.__conn.keys(pattern)
    def rpush(self,List,value):
        return self.__conn.rpush(List,value)    #把值插入列表尾部
    def llen(self,List):
        return self.__conn.llen(List)
    def lpop(self,List):
        return self.__conn.lpop(List)

class RedisHelper2:
    def __init__(self):
        self.__conn = redis.Redis(host=settings.REDIS_CONN['HOST'],port=6379,db=0,password=settings.REDIS_CONN['PASSWD'])
        self.chan_sub = 'fm107.8'
        self.chan_pub = 'fm107.8'
    def get(self,key):
        return self.__conn.get(key)
    def set(self,key,value):
        return self.__conn.set(key,value)
    def set_300(self,key,value,timeout):
        return self.__conn.set(key,value,timeout)
    def public(self,msg):
        self.__conn.publish(self.chan_pub,msg)
        return True
    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
    def lrange(self,key,start,end):
        return self.__conn.lrange(key,start,end)
    def keys(self,pattern):
        return self.__conn.keys(pattern)
    def rpush(self,List,value):
        return self.__conn.rpush(List,value)    #把值插入列表尾部

if __name__ == '__main__':
    t = RedisHelper()
    t.public('test')    #127.0.0.1:6379 > SUBSCRIBE 104.5
