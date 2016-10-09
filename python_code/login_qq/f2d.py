#coding:utf-8
import re

def f2d(string):
    '转换表单数据为字典'
    l1 = re.findall(r'(?m)^[\w-]+',string)
    l2 = re.findall(r'(?<=:).*',string)
    return dict(zip(l1,l2))

if __name__ == '__main__':
    s = '''
backurl:http://www.baidu.com
action:newlogin
loginby:0
logintype:0
txtNAME:111111111111
txtPassword:111111111111
safecode:
randomcode:0190
x:41
y:13
'''
    for e in f2d(s).items():
        print(e)
