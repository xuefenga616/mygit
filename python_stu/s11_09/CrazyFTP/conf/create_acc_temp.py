#coding:utf-8
__author__ = 'xuefeng'
import json

acc_dic = {
    'alex': {'password':'123456', 'quotation': 1000000, 'expire_date': "2017-01-01"},
    'xuefeng': {'password':'123456', 'quotation': 1000000, 'expire_date': "2017-01-01"},
    'dali': {'password':'123456', 'quotation': 1000000, 'expire_date': "2017-01-01"},
}

with file('accounts.json','wb') as f:
    json.dump(acc_dic,f)