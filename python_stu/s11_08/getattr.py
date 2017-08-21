#coding:utf-8
__author__ = 'Administrator'

"""
models:数据库
views:html模板
controllers:逻辑处理
"""

#url = raw_input("url:")
print dir(getattr)  # 查看getattr所用方法

#动态加载模块
a = ['test.yaml','test.txt']
module = __import__("re")
func = getattr(module,'search')
print [i for i in a if func('.yaml$',i)][0]