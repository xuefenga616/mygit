#coding:utf-8
__author__ = 'xuefeng'
import threading,Queue

class ThreadPool(object):
    def __init__(self,max_num):
        self.queue = Queue.Queue(max_num)
        for i in xrange(max_num):
            self.queue.put(threading.Thread)

    def get_thread(self):
        return self.queue.get()

    def add_thread(self):
        self.queue.put(threading.Thread)

pool = ThreadPool(10)

def func(arg,p):
    print arg
    import time
    time.sleep(2)
    p.add_thread()

for i in xrange(30):
    thread = pool.get_thread()  #即thread = threading.Thread()
    t = thread(target=func,args=(i,pool))
    t.start()
