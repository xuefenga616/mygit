#coding:utf-8
__author__ = 'Administrator'

import time

def json_date_handle(obj):
    if hasattr(obj,'isoformat'):
        return obj.strftime("%Y-%m-%d %H:%M:%S")

def json_date_to_stamp(obj):
    if hasattr(obj,'isoformat'):
        return time.mktime(obj.timetuple()) * 1000
