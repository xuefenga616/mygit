#coding:utf-8
__author__ = 'xuefeng'
from multiprocessing import Process,Pool
import time

def foo(i):
    time.sleep(2)
    return i + 100

def bar(arg):
    print arg

pool = Pool(5)
for i in range(10):
    pool.apply_async(func=foo,args=(1,),callback=bar)

print 'end'
pool.close()
pool.join()
