#coding:utf-8
__author__ = 'xuefeng'
import time
from jinja2 import Template

def index():
    data = open('Views/index.html').read()
    cur_time = str(time.time())
    user_list = ['alex','eric']
    template = Template(data)
    result = template.render(name='alex',age='23',cur_time=cur_time,user_list=user_list,num=1)    #模板替换的过程
    return result.encode('utf-8')

def login():
    data = open('Views/login.html').read()
    return data