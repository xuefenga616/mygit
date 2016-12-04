#coding:utf-8
__author__ = 'xuefeng'

from redis_conn import RedisHelper as redis
from redis_conn import RedisHelper2 as redis2
import pickle,time,json
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

            uptime_in_redis_key = 'StatusData_%s_uptime_latest' %client_id
            last_point_from_redis = self.redis.lrange(uptime_in_redis_key,-1,-1)
            if not last_point_from_redis:
                self.redis.rpush(uptime_in_redis_key,json.dumps(time.time()))

            data_saving_obj = data_optimization.DataStore(self.redis,client_id,service_name,data)

            #在这里触发监控
            host_obj = models.Host.objects.get(id=client_id)
            service_triggers = serializer.get_host_triggers(host_obj)

            trigger_handler = data_processing.DataHandler(self.redis)
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
            matched_action_list = set()
            for action in actions_set:
                #每个action都可以包含多个主机或主机组
                #print 'action: ',action
                for g in action.host_groups.select_related():
                    for h in g.host_set.select_related():
                        if h.id == host_id:     #这个action适用于此主机
                            matched_action_list.add(action)
                            if action.id not in self.alert_counter_dic: #第一次被触发，先初始化一个action_counter_dic
                                self.alert_counter_dic[action.id] = {h.id:{'counter':0,'last_alert':time.time()}}
                            if h.id not in self.alert_counter_dic[action.id]:
                                self.alert_counter_dic[action.id][h.id] = {'counter':0,'last_alert':time.time()}
                for h in action.hosts.select_related():
                    if h.id == host_id:     #这个action适用于此主机
                        matched_action_list.add(action)
                        # self.alert_counter_dic.setdefault(action, {h.id:{'counter':0,'last_alert':time.time()}})
                        if action.id not in self.alert_counter_dic: #第一次被触发，先初始化一个action_counter_dic
                            self.alert_counter_dic[action.id] = {h.id:{'counter':0,'last_alert':time.time()}}
                        if h.id not in self.alert_counter_dic[action.id]:
                            self.alert_counter_dic[action.id][h.id] = {'counter':0,'last_alert':time.time()}
            print self.alert_counter_dic

            for action_obj in matched_action_list:
                #print action_obj.interval   #告警设置里的告警间隔
                if time.time() - self.alert_counter_dic[action_obj.id][host_id]['last_alert'] >= action_obj.interval:
                    #该报警了
                    for action_operation in action_obj.operations.select_related().order_by('-step'):  #step是第n次告警
                        if action_operation.step > self.alert_counter_dic[action_obj.id][host_id]['counter']:
                            self.alert_counter_dic[action_obj.id][host_id]['counter'] += 1  #发一次邮件就不发了
                            for user in action_operation.notifiers.select_related():
                                print "alert action:%s" %action_operation.action_type,user.name

                if time.time() - self.alert_counter_dic[action_obj.id][host_id]['last_alert'] >= 3600:
                    self.alert_counter_dic[action_obj.id][host_id]['counter'] = 0
                    self.alert_counter_dic[action_obj.id][host_id]['last_alert'] = time.time()
