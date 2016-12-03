#coding:utf-8
__author__ = 'xuefeng'

import time
from conf import settings
import urllib,urllib2
import json
import threading
from plugins import plugin_api
import os,sys
import pickle
from redis_conn import RedisHelper as redis

class ClientHandle(object):
    def __init__(self):
        self.monitored_services = {}
        self.redis = redis()
    def load_latest_configs(self):
        request_type = settings.configs['urls']['get_configs'][1]
        url = '%s/%s' %(settings.configs['urls']['get_configs'][0],settings.configs['HostID'])
        latest_configs = self.url_request(request_type,url)
        latest_configs = json.loads(latest_configs)
        self.monitored_services.update(latest_configs)  #合并字典

    def url_request(self,request_type,url,**extra_data):
        abs_url = "http://%s:%s/%s" %(settings.configs['Server'],
                                      settings.configs['ServerPort'],
                                      url)
        if request_type in ('get','GET'):
            print abs_url,extra_data
            try:
                req = urllib2.Request(abs_url)
                req_data = urllib2.urlopen(req,timeout=settings.configs['RequestTimeout'])
                callback = req_data.read()
                #print "--->server response:",callback
                return callback
            except urllib2.URLError,e:
                sys.exit("\033[31;1m %s\033[0m" %e)
        elif request_type in ('post','POST'):
            try:
                data_encode = urllib.urlencode(extra_data['params'])
                req = urllib2.Request(url=abs_url,data=data_encode)
                res_data = urllib2.urlopen(req,timeout=settings.configs['RequestTimeout'])
                callback = res_data.read()
                callback = json.loads(callback)
                print "\033[31;1m [%s]:[%s]\033[0m response:\n%s" %(request_type,abs_url,callback)
                return callback
            except Exception,e:
                sys.exit("\033[31;1m %s\033[0m" %e)

    def forever_run(self):
        exit_flag = False
        config_last_update_time = 0
        while not exit_flag:
            if time.time() - config_last_update_time > settings.configs['ConfigUpdateInterval']: #配置每300s更新一次
                self.load_latest_configs()
                print "Loaded latest config:",self.monitored_services
                config_last_update_time = time.time()   #更新配置时间戳

            for service_name,val in self.monitored_services['services'].items():
                if len(val) == 2:   #第一次启动客户端，如：val=[u'get_linux_cpu', 60]
                    self.monitored_services['services'][service_name].append(0)   #加上初始时间戳0
                monitor_interval = val[1]   #监控间隔
                last_invoke_time = val[2]   #时间戳
                if time.time() - last_invoke_time > monitor_interval:   #超时
                    self.monitored_services['services'][service_name][2] = time.time() #更新每个监控项的时间戳，即last_invoke_time
                    #开始一个新线程运行插件
                    t = threading.Thread(target=self.invoke_plugin,args=(service_name,val))
                    t.start()
                    print "Going to monitor [%s]" %service_name
                else:
                    wait_time = monitor_interval + last_invoke_time - time.time()
                    print "Going to monitor [%s] in [%s] secs" %(service_name,wait_time)
            time.sleep(2)

    def invoke_plugin(self,service_name,val):
        plugin_name = val[0]
        if hasattr(plugin_api,plugin_name):
            func = getattr(plugin_api,plugin_name)
            plugin_callback = func()

            #开始上报数据
            report_data = {
                'client_id': settings.configs['HostID'],
                'service_name': service_name,
                'data': plugin_callback
            }
            report_data = pickle.dumps({'report_service_data':report_data})
            #print "report data:",report_data

            self.redis.public(report_data)

            #request_action = settings.configs['urls']['service_report'][1]
            #request_url = settings.configs['urls']['service_report'][0]
            #self.url_request(request_action,request_url,params=report_data)

        else:
            print "\033[31;1m Cannot find plugin names [%s] in plugin_api\033[0m" %plugin_name


