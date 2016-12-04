#coding:utf-8
__author__ = 'xuefeng'

import models
import json,time
from django.core.exceptions import ObjectDoesNotExist
from backends.redis_conn import RedisHelper as redis
from backends.redis_conn import RedisHelper2 as redis2

class ClientHandler(object):
    def __init__(self,client_id):
        self.client_id = client_id
        self.client_configs = {
            "services": {}
        }
    def fetch_configs(self):
        try:
            host_obj = models.Host.objects.get(id=self.client_id)
            template_list = list(host_obj.templates.select_related())

            for g in host_obj.host_groups.select_related():
                template_list.extend(g.templates.select_related())
            #print  template_list
            for template in template_list:
                for service in template.services.select_related():
                    #print service
                    self.client_configs['services'][service.name] = [service.plugin_name,service.interval]
        except ObjectDoesNotExist:
            pass
        return self.client_configs

class TriggersView(object):
    def __init__(self,request):
        self.request = request
        self.redis = redis()
    def fetch_related_filters(self):
        by_host_id = self.request.GET.get('by_host_id')
        print '---host id:',by_host_id
        host_obj = models.Host.objects.get(id=by_host_id)
        trigger_dic = {}
        if by_host_id:
            trigger_match_keys = "host_%s_trigger_*" %by_host_id
            trigger_keys = self.redis.keys(trigger_match_keys)
            print "trigger keys:",trigger_keys
            for key in trigger_keys:
                data = json.loads(self.redis.get(key))
                if data.get('trigger_id'):  #正经trigger数据
                    trigger_obj = models.Trigger.objects.get(id=data.get('trigger_id'))
                    data['trigger_obj'] = trigger_obj
                data['host_obj'] = host_obj
                trigger_dic[key] = data

        return trigger_dic

def get_host_triggers(host_obj):
    triggers = []
    for template in host_obj.templates.select_related():
        triggers.extend(template.triggers.select_related())
    for g in host_obj.host_groups.select_related():
        for template in g.templates.select_related():
            triggers.extend(template.triggers.select_related())
    return set(triggers)

class StatusSerializer(object):
    def __init__(self,request):
        self.request = request
        self.redis = redis()
    def by_hosts(self):
        host_obj_list = models.Host.objects.all()
        host_data_list = []
        for h in host_obj_list:
            host_data_list.append(self.single_host_info(h))
        return host_data_list
    def single_host_info(self,host_obj):
        data = {
            'id': host_obj.id,
            'name': host_obj.name,
            'ip_addr': host_obj.ip_addr,
            'status': host_obj.get_status_display(),
            'uptime': None,
            'last_update': None,
            'total_services': None,
            'ok_nums': None,
        }

        uptime = self.get_host_uptime(host_obj)     #
        if uptime:
            print 'uptime:', uptime[0],uptime[1]
            data['uptime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(uptime[0])))
            data['last_update'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(uptime[1])))

        #for triggers
        data['triggers'] = self.get_triggers(host_obj)
        return data
    def get_host_uptime(self,host_obj):
        redis_key = 'StatusData_%s_uptime_latest' %host_obj.id
        # last_data_point = self.redis.lrange(redis_key,-1,-1)
        last_data_point = self.redis.lrange(redis_key,0,-1)

        return last_data_point

    def get_triggers(self,host_obj):
        trigger_keys = self.redis.keys('host_%s_trigger_*' %host_obj.id)
        '''
        (1,'Information'),
        (2,'Warning'),
        (3,'Average'),
        (4,'High'),
        (5,'Diaster'),
        '''
        trigger_dic = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
        }

        for trigger_key in trigger_keys:
            trigger_data = self.redis.get(trigger_key)
            if trigger_key.endswith("None"):
                trigger_dic[4].append(json.loads(trigger_data))
            else:
                trigger_id = trigger_key.split('_')[-1]
                trigger_obj = models.Trigger.objects.get(id=trigger_id)
                trigger_dic[trigger_obj.severity].append(json.loads(trigger_data))
        print "trigger data:", trigger_dic
        return trigger_dic