#coding:utf-8
__author__ = 'xuefeng'
from multiprocessing import Process
import time

def foo(i):
    print "say hi",i
    time.sleep(1)

for i in range(10):
    p = Process(target=foo,args=(i,))
    p.start()
