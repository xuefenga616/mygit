#coding:utf-8
__author__ = 'xuefeng'

import models
import json
from backends.redis_conn import RedisHelper2 as redis2

class GraphGenerator(object):   #产生流量图
    def __init__(self,request):
        self.request = request
        self.redis2 = redis2()
        self.host_id = self.request.GET.get('host_id')
        self.time_range = self.request.GET.get('time_range')    #获取要从redis中取多长时间的数据，单位是min，eg:10min

    def get_host_graph(self):
        host_obj = models.Host.objects.get(id=self.host_id)
        service_data_dic = {}
        template_list = list(host_obj.templates.select_related())
        for g in host_obj.host_groups.select_related():
            template_list.extend(list(host_obj.templates.select_related()))
        template_list = set(template_list)

        for template in template_list:
            for service in template.services.select_related():
                service_data_dic[service.id] = {
                    'name': service.name,
                    'index_data': {},
                    'has_sub_service': service.has_sub_services,
                    'raw_data': [],
                    'items': [item.key for item in service.items.select_related()]
                }
                '''if not service.has_sub_service'''

        print service_data_dic

        for service_id,val_dic in service_data_dic.items():
            service_redis_key = "StatusData_%s_%s_%s" %(self.host_id,val_dic['name'],self.time_range)
            print 'service_redis_key',service_redis_key
            service_raw_data = self.redis2.lrange(service_redis_key,0,-1)
            service_data_dic[service_id]['raw_data'] = service_raw_data
        return service_data_dic
