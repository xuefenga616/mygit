#coding:utf-8
__author__ = 'Administrator'

n1 = 10
s1 = "123"

print isinstance(n1,int)    #返回true
print isinstance(s1,str)

class A:
    pass

class B(A):
    pass

b = B()
print isinstance(b,A)   #返回true,表示b是类B的基类的实例
print issubclass(B,A)

