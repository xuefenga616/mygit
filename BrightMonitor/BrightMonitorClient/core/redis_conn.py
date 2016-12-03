#coding:utf-8
__author__ = 'xuefeng'
import os,sys
import redis

class RedisHelper:
    def __init__(self):
        self.__conn = redis.Redis(host='192.168.1.13',port=6379,db=0,password='123456')
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

if __name__ == '__main__':
    t = RedisHelper()
    t.public('test')    #127.0.0.1:6379 > SUBSCRIBE 104.5
