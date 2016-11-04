#coding:utf-8

from conf import settings
import sys
import MySQLdb

class MysqlConn(object):
    def __init__(self):
        self.__conn = MySQLdb.connect(host=settings.DATABASE['host'],
                                      port=settings.DATABASE['port'],
                                      user=settings.DATABASE['username'],
                                      passwd=settings.DATABASE['password'],
                                      db=settings.DATABASE['db_name'])
        self.__cursor = self.__conn.cursor()
    def select(self,query,argv=None):
        try:
            self.__cursor.execute(query,argv)
            res = self.__cursor.fetchall()
            return  res
        except MySQLdb.Error,e:
            print "\033[31;1m%s\033[0m" % e
    def execute(self,query,argv=None):
        try:
            self.__cursor.execute(query)
        except MySQLdb.Error,e:
            print "\033[31;1m%s\033[0m" % e
    def insert(self,query,argv=None):
        try:
            self.__cursor.execute(query,argv)
            self.__conn.commit()
        except MySQLdb.Error,e:
            print "\033[31;1m%s\033[0m" % e
    def insert_many(self,query,argv=None):
        try:
            self.__cursor.executemany(query,argv)
            self.__conn.commit()
            return True
        except MySQLdb.Error,e:
            print "\033[31;1m%s\033[0m" % e
    def select_many(self,query,argv=None):
        try:
            self.__cursor.executemany(query,argv)
            return self.__cursor.fetchall()
        except MySQLdb.Error,e:
            print "\033[31;1m%s\033[0m" % e
    def __del__(self):
        self.__cursor.close()
        self.__conn.commit()
        self.__conn.close()
        