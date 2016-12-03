#coding:utf-8
__author__ = 'xuefeng'

configs = {
    'HostID': 7,
    'Server': '192.168.1.17',
    'ServerPort': 8001,
    'urls': {
        'get_configs': ['api/client/config','get'],
        'service_report': ['api/client/service/report','post'],
    },
    'RequestTimeout': 30,
    'ConfigUpdateInterval': 300,    #5分钟更新一次监控配置
}