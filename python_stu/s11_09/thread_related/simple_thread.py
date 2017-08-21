#coding:utf-8
__author__ = 'xuefeng'
import threading,time

def run(num):
    time.sleep(1)

    lock.acquire()     #获取锁
    print "thread...",num
    lock.release()      #释放锁

lock = threading.Lock()     #加锁

for i in range(100):
    t = threading.Thread(target=run,args=(i,))
    t.start()


