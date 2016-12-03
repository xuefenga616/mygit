#coding:utf-8
__author__ = 'xuefeng'

from redis_conn import RedisHelper as redis
from redis_conn import RedisHelper2 as redis2
import pickle,time
from monitor import models
import data_optimization
from monitor import serializer
from backends import data_processing

class TriggerHandler(object):
    def __init__(self):
        self.alert_cnts = {}    #记录每个action的触发报警次数
        alert_cnts = {
            1: {2: {'counter': 0, 'last_alert': None},
                4: {'counter': 1, 'last_alert': None}},     #k是action_id, {2:0,3:2}这里面k是主机id,value是报警次数
        }

    def start_watching(self):
        self.redis2 = redis2()
        redis_sub2 = self.redis2.subscribe()  #订阅trigger消息
        #print "\033[43;1m*******start listening new triggers*******\033[0m"
        self.trigger_cnt = 0
        while True:
            trigger_msg = redis_sub2.parse_response()
            self.trigger_consume(trigger_msg)

    def trigger_consume(self,trigger_msg):
        self.trigger_cnt += 1

        trigger_msg = pickle.loads(trigger_msg[2])  #index2才是数据
        print "\033[41;1m*******Got a trigger msg [%s]*******\033[0m" %self.trigger_cnt
        #print trigger_msg['positive_expressions'][0]['expression_obj']
        action = ActionHandler(trigger_msg,self.alert_cnts)
        action.trigger_process()

    def start(self):
        self.redis = redis()
        redis_sub = self.redis.subscribe()  #订阅report消息
        while True:
            msg = redis_sub.parse_response()
            msg = pickle.loads(msg[2])
            self.service_data_report(msg)

    def service_data_report(self,msg):
        try:
            report_msg = msg['report_service_data']
            #print report_msg
            client_id = report_msg['client_id']
            service_name = report_msg['service_name']
            data = report_msg['data']

            data_saving_obj = data_optimization.DataStore(client_id,service_name,data)

            #在这里触发监控
            host_obj = models.Host.objects.get(id=client_id)
            service_triggers = serializer.get_host_triggers(host_obj)

            trigger_handler = data_processing.DataHandler(connect_redis=False)
            for trigger in service_triggers:
                trigger_handler.load_service_data_and_calulating(host_obj,trigger)
            print "service trigger::",service_triggers

        except IndexError,e:
            print "----->err:",e


class ActionHandler(object):
    '''
    负责把达到报警条件的trigger进行分析，并根据action表中的配置来进行报警
    '''
    def __init__(self,trigger_data,alert_counter_dic):
        self.trigger_data = trigger_data
        self.alert_counter_dic = alert_counter_dic
    def trigger_process(self):  #分析trigger并报警
        print "Action Processing".center(50,'-')    #打个显眼的分隔符
        print self.trigger_data
        if self.trigger_data.get('trigger_id') == None: #既然没有trigger_id，直接报警
            if self.trigger_data.get('msg'):    #eg: linux_memory_warning
                print self.trigger_data.get('msg')
            else:
                print "\033[41;1m Invalid trigger data %s\033[0m" %self.trigger_data
        else:   #正经的trigger
            trigger_id = self.trigger_data.get('trigger_id')
            host_id = self.trigger_data.get('host_id')
            trigger_obj = models.Trigger.objects.get(id=trigger_id)
            actions_set = trigger_obj.action_set.select_related()   #反向找到这个trigger所关联的action list(m2m)
            matched_action_list = {}
            #print actions_set
            #################################
            ##################################
            #################################

