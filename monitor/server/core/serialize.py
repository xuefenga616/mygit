#_*_coding:utf-8_*_

import global_settings
from conf.hosts import monitored_groups
import pickle,time
from redishelper import RedisHelper

def host_config_serializer(host_ip):
    applied_services = []
    for group in monitored_groups:
        if host_ip in group.hosts:
            applied_services.extend(group.services) #后面追加列表，group.services是一台主机所有配置的服务
    applied_services = set(applied_services)    #去重，列表转集合去掉重复项

    configs = {     #等下以字典格式传给客户端
        'services': {},
        #'refresh_configs_interval':
    }
    for service in applied_services:
        service = service() #把类实例化
        configs['services'][service.name] = [
            service.interval,
            service.plugin_name,
            0,  #放最后运行的时间last_check
        ]
    return configs

def flush_all_host_configs_into_redis():    #把所有配置刷到redis
    applied_hosts = []
    redis = RedisHelper()
    for group in monitored_groups:
        applied_hosts.extend(group.hosts)
    applied_hosts = set(applied_hosts)

    for host_ip in applied_hosts:
        host_config = host_config_serializer(host_ip)
        # 序列化字典后存入redis
        key = 'HostConfig::%s' %host_ip
        redis.set(key, pickle.dumps(host_config))

def report_service_data(server_instance,msg):
    host_ip = msg['ip']
    service_status_data = msg['data']
    service_name = msg['service_name']

    server_instance.hosts['hosts'][host_ip][service_name] ={
                    'data':service_status_data,
                    'time_stamp': time.time()
                    }
    key = 'StatusData::%s' % host_ip
    server_instance.redis.set(key, pickle.dumps(server_instance.hosts['hosts'][host_ip]))

def all_host_configs():
    configs ={'hosts': {}}
    for group in monitored_groups:
        for host_ip in group.hosts:
            #if not configs['hosts'].has_key(host_ip):
            configs['hosts'][host_ip]= {}
    return  configs

if __name__ == '__main__':
    #host_config_serializer('192.168.1.12')
    flush_all_host_configs_into_redis()