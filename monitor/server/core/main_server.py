#_*_coding:utf-8_*_

import global_settings
from redishelper import RedisHelper
import serialize
import action_process
import time,pickle
from conf.hosts import monitored_groups

class MonitorServer(object):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.hosts = serialize.all_host_configs()
        self.redis = RedisHelper()
    def get_config(self,host):
        applied_services = []
        config_list = {host:{}}
        for group in monitored_groups:
            if host in group.hosts:
                applied_services.extend(group.services) #后面追加列表，group.services是一台主机所有配置的服务
        applied_services = set(applied_services)    #去重，列表转集合去掉重复项
        for service in applied_services:
            service = service() #把类实例化
            config_list[host][service.name] = service.triggers
        #print config_list
        return config_list[host]


    def handle(self):
        redis_sub = self.redis.subscribe()

        value_dic = {}
        for host in self.hosts['hosts'].keys():
            value_dic[host] = {
                'MemUsage':[],
                'iowait':[], 'idle':[],
                'load1':[]
            }      #用来存数据
        print value_dic

        while True:
            msg= redis_sub.parse_response()
            #print 'recv:',msg
            action_process.action_process(self,msg) #self是将本实例传给action_process方法，action_process不再需要导入redis
            print '----waiting for new msg ---'

            #received data
            for host,val in self.hosts['hosts'].items():
                if val is not None:
                    #print host, val
                    #get config
                    configs = self.get_config(host)

                    for service_name,val2 in val.items():
                        print "hahaha",configs[service_name]
                        c_time_stamp = val2['time_stamp']
                        data = val2['data']
                        #print "dadada",data

                        time_pass_since_last_recv = time.time() - c_time_stamp
                        #print  "Time pass:",time_pass_since_last_recv
                        if time_pass_since_last_recv >= 30:
                            #设定30秒超时
                            print "\033[41;1m Service %s has no data for %ss\033[0m" %(service_name,time_pass_since_last_recv)
                        else:

                            if 'MemUsage' in data.keys():
                                key = 'MemUsage'
                                key_value = int(data['MemUsage']) * 100 / int(data['MemTotal'])
                                print key,": ",key_value
                                value_dic[host][key].append(float(key_value))
                            else:
                                for key in configs[service_name].keys():
                                    key_value = data[key]
                                    print key,": ",key_value
                                    value_dic[host][key].append(float(key_value))
                        for key in configs[service_name].keys():
                            if len(value_dic[host][key]) > 5:  #只保留5个数，测试用
                                del value_dic[host][key][0]
                                configs[service_name][key]['func'](configs[service_name][key]['warning'],configs[service_name][key]['operator'],value_dic[host][key][-6:-1])
                            #times = int(configs[service_name][key]['minutes'])*60/
                            print value_dic



    def run(self):
        print '----starting monitor server----'
        self.handle()

    def process(self):
        pass


if __name__=='__main__':
    s = MonitorServer('192.168.1.12','6379')
    s.run()

    