#_*_coding:utf-8_*_

import pickle 
from redishelper import RedisHelper
import threading
from plugins import plugin_api
import time

host_ip = '192.168.1.13'
class MonitorClient(object):
    def __init__(self,server,port):
        self.server = server
        self.port = port
        self.configs = {}
        self.redis = RedisHelper()   #建立redis链接
    def format_msg(self,key,value):     #专门用来处理数据
        msg = {key: value}
        return pickle.dumps(msg)
    def get_configs(self):
        config = self.redis.get('HostConfig::%s' %self.server)
        if config:  #redis里存在此key
            self.configs = pickle.loads(config)
            return True
    def handle(self):
        if self.get_configs():
            print "--- going to monitor services ---",self.configs
            #开始监控
            while True:
                for service_name,val in self.configs['services'].items():
                    #print service_name,val
                    interval,plugin_name,last_check = val
                    if time.time() - last_check >= interval:    #代表超时，需要启一个新线程运行了
                        t = threading.Thread(target=self.task,args=[service_name,plugin_name])
                        t.start()
                        self.configs['services'][service_name][2] = time.time() #更新时间戳
                    else:
                        next_run_time = interval + last_check - time.time()
                        print "%s will be run in next %s seconds" %(service_name,next_run_time)
                time.sleep(2)
        else:
            print "--- could not found any configurations for this host ---"
    def task(self,service_name,plugin_name):
        print "---going to run service:",service_name,plugin_name
        func = getattr(plugin_api,plugin_name)
        result = func() #执行插件
        #把执行结果发给redis
        #self.redis.publish(pickle.dumps(result))
        msg = self.format_msg('report_service_data',
                              {'ip':host_ip,
                               'service_name':service_name,
                               'data':result})
        self.redis.public(msg)
    def run(self):
        self.handle()

if __name__ == '__main__':
    cli = MonitorClient(host_ip,'port')
    cli.run()
    
