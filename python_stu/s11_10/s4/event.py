#coding:utf-8
__author__ = 'xuefeng'
import threading
import time

def do(event):
    """
    判断flag
    flag = True = set()
    flag = False = clear()
    """
    print "start"
    event.wait()
    print "execute"

event_obj = threading.Event()

for i in range(10):
    t = threading.Thread(target=do,args=(event_obj,))
    t.start()

event_obj.clear()
inp = raw_input("input:")
if inp == "true":
    event_obj.set()