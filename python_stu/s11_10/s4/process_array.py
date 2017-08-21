#coding:utf-8
__author__ = 'xuefeng'
from multiprocessing import Process,Array

#创建一个只包含数字类型的一个列表，列表个数不可变
tmp = Array('i',[11,22,33,44])

def foo(i):
    tmp[i] = 100 + i
    for item in tmp:
        print i,"---->",item

for i in range(4):
    p = Process(target=foo,args=(i,))
    p.start()