#coding:utf-8
__author__ = 'xuefeng'
import Queue

# obj = object()
#
# q = Queue.Queue()
# for i in range(10):
#     print id(obj)
#     q.put(obj)

"""
1、主线程
2、子线程1 =》专门用来打印正在执行线程个数
3、20次循环，创建20个线程，线程内部进行操作
"""

import contextlib
import time
import threading
import random

doing = []
def num(l2):
    while True:
        print len(l2)
        time.sleep(1)
t = threading.Thread(target=num,args=(doing,))
t.start()

@contextlib.contextmanager  #管理上下文
def show(l1,item):
    #print 'before'
    doing.append(item)
    yield
    doing.remove(item)
    #print 'after'

print len(doing)

def task(i):
    flag = threading.current_thread()
    with show(doing,flag):     #上下文
        print "with in"
        print len(doing)
        time.sleep(random.randint(1,10))

for i in range(20):
    tmp = threading.Thread(target=task,args=(i,))
    tmp.start()