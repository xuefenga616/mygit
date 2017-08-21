#coding:utf-8
__author__ = 'xuefeng'
import threading,time

def run(num):
    time.sleep(1)

    semaphore.acquire()     #获取锁
    print "thread...",num
    semaphore.release()      #释放锁

semaphore = threading.BoundedSemaphore(5)   #信号量,可以同时有5个线程

for i in range(100):
    t = threading.Thread(target=run,args=(i,))
    t.start()

while threading.active_count() != 1:    #程序本身会起一个线程
    print "current thread num: ",threading.active_count()      #打印当前活动线程
else:
    print "----all theads done----"



