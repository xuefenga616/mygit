#coding:utf-8
__author__ = 'xuefeng'
import select
import threading
import sys

while True:
    """
    如果用户输入内容,select感知sys.stdin改变,
    将改变的文件句柄保存至列表,并将列表作为select第一个参数返回
    如果用户未输入内容,select第一个参数 = []
    """
    readable,writeable,error = select.select([sys.stdin,sys.stdout,],[],[],1)

    if sys.stdin in readable:
        print "select get stdin:",sys.stdin.readline()

