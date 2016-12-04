#coding: utf-8
__author__ = 'xuefeng'
import os,sys

basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)
sys.path.append('%s/BrightMonitor' %basedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'BrightMonitor.settings'
import django
django.setup()

import time,json,pickle
from BrightMonitor import settings
from monitor import models
from redis_conn import RedisHelper as redis
from redis_conn import RedisHelper2 as redis2
import operator
from BrightMonitorClient.plugins import plugin_api
from BrightMonitorClient.conf import settings as c_settings
import threading

class DataHandler(object):
    def __init__(self,main_ins):
        self.poll_interval = 20
        self.config_update_interval = 120
        self.config_last_loading_time = time.time() #当时时间戳
        self.global_monitor_dic = {}
        self.exit_flag = False
        #if connect_redis:
        self.redis = main_ins

    def looping(self):
        self.update_or_load_configs()   #生成全局的监控配置dict
        print self.global_monitor_dic

        cnt = 0
        while not self.exit_flag:
            print "looping %s".center(50,'-') %cnt  #打印分隔符
            cnt += 1
            if time.time() - self.config_last_loading_time >= self.config_update_interval: #2分钟更新一次主机状态
                print "\033[41;1m need update configs...\033[0m"
                self.update_or_load_configs()
            if self.global_monitor_dic:
                for h,config_dic in self.global_monitor_dic.items():
                    print "handling host:\033[32;1m%s\033[0m" %h
                    for service_id,val in config_dic['services'].items():   #循环所有要监控的服务
                        #print service_id,val
                        service_obj,last_monitor_time = val
                        #print "<------>",service_obj.plugin_name
                        if time.time() - last_monitor_time >= service_obj.interval: #到了再发起监控时间
                            print "Going to monitor [%s]" %service_obj.name
                            self.global_monitor_dic[h]['services'][service_obj.id][1] = time.time() #更新dict监控项时间戳
                            #self.data_point_validation(h,service_obj)   #检测此服务最近的汇报数据
                        else:
                            next_monitor_time = last_monitor_time + service_obj.interval - time.time()
                            print "service [%s] next monitor time is %s" %(service_obj.name,next_monitor_time)

                    if time.time() - self.global_monitor_dic[h]['status_last_check'] > 10:
                        #检测有没有这个机器的trigger，如果没有，把主机状态改成ok
                        trigger_redis_key = "host_%s_trigger" %h.id
                        trigger_keys = self.redis.keys(trigger_redis_key)
                        if len(trigger_keys) == 0:  #没有trigger被触发，可以把状态改成ok了
                            h.status = 1
                            h.save()

            time.sleep(self.poll_interval)

    def update_or_load_configs(self):
        '''
        load monitor configs from MySQL db
        '''
        all_enabled_hosts = models.Host.objects.all()
        for h in all_enabled_hosts:
            if h not in self.global_monitor_dic:    #new host
                self.global_monitor_dic[h] = {'services':{}, 'triggers':{}}
            #print h.host_groups.select_related()

            service_list = []
            trigger_list = []
            for g in h.host_groups.select_related():
                #print "grouptemplates:",g.templates.select_related()
                for template in g.templates.select_related():
                    service_list.extend(template.services.select_related()) #合并列表
                    trigger_list.extend(template.triggers.select_related())
                for service in service_list:
                    if service.id not in self.global_monitor_dic[h]['services']:    #first loop
                        self.global_monitor_dic[h]['services'][service.id] = [service, 0]   #加入初始时间戳0
                    else:
                        self.global_monitor_dic[h]['services'][service.id][0] = service
                for trigger in trigger_list:
                    self.global_monitor_dic[h]['triggers'][trigger.id] = trigger
            #print 'service list:', service_list

            for template in h.templates.select_related():
                service_list.extend(template.services.select_related()) #合并列表
                trigger_list.extend(template.triggers.select_related())
            for service in service_list:
                if service.id not in self.global_monitor_dic[h]['services']:    #first loop
                    self.global_monitor_dic[h]['services'][service.id] = [service, 0]   #加入初始时间戳0
                else:
                    self.global_monitor_dic[h]['services'][service.id][0] = service
            for trigger in trigger_list:
                self.global_monitor_dic[h]['triggers'][trigger.id] = trigger
            #print self.global_monitor_dic[h]
            #通过这个时间来确定是否需要更新主机状态
            self.global_monitor_dic[h].setdefault('status_last_check', time.time()) #键不存在时，设置默认键值

        self.config_last_loading_time = time.time()
        return True

    def load_service_data_and_calulating(self,host_obj,trigger_obj):
        '''
        :param host_obj
        :param trigger_obj
        :return
        '''
        #self.redis = redis()
        calc_sub_res_list = []  #先把每个expression的结果算出来放在这个列表里，最后再统一计算这个列表
        positive_expressions = []
        expression_res_string = ''
        for expression in trigger_obj.triggerexpression_set.select_related().order_by('id'):
            print expression, expression.logic_type
            expression_process_obj = ExpressionProcess(self,host_obj,expression)
            single_expression_res = expression_process_obj.process()
            if single_expression_res:
                calc_sub_res_list.append(single_expression_res)
                if single_expression_res['expression_obj'].logic_type:  #不是最后一条，条件关系最后一条没选是None
                    expression_res_string += str(single_expression_res['calc_res']) + ' ' + \
                                            single_expression_res['expression_obj'].logic_type + ' '
                else:
                    expression_res_string += str(single_expression_res['calc_res']) + ' '

                #把所有结果为True的expression提取出来，报警时你就知道什么问题导致trigger触发了
                if single_expression_res['calc_res'] == True:
                    single_expression_res['expression_obj'] = single_expression_res['expression_obj'].id #要存到redis，数据库对象转成id
                    positive_expressions.append(single_expression_res)
        if expression_res_string:
            trigger_res = eval(expression_res_string)   #取string第一个值
            print "whole trigger res:", trigger_res
            if trigger_res:     #此时触发了报警
                print "##############trigger alert:",trigger_obj.severity,trigger_res
                self.trigger_notifier(host_obj,trigger_obj.id,positive_expressions,msg=trigger_obj.name)    #msg需要专门分析后生成


    def data_point_validation(self,host_obj,service_obj):
        service_redis_key = "StatusData_%s_%s_latest" %(host_obj.id,service_obj.id)  #拼出此服务在redis中存储对应的key
        latest_data_point = self.redis.lrange(service_redis_key,-1,-1)
        if latest_data_point:   #data list is not empty
            pass
        else:   #no data at all
            print "\033[41;1m no data for service [%s] host[%s] at all..\033[0m" %(service_obj.name,host_obj.name)
            msg = "no data for service [%s] host[%s] at all.." %(service_obj.name,host_obj.name)
            self.trigger_notifier(host_obj=host_obj,trigger_id=None,positive_expressions=None,msg=msg)
            host_obj.status = 5     #problem
            host_obj.save()

    def trigger_notifier(self,host_obj,trigger_id,positive_expressions,msg=None):
        '''
        :param host_obj
        :param trigger_id
        :param positive_expressions: it's list,contains all the expression has True result
        :param msg
        :return
        '''
        self.redis2 = redis2()      #redis2 是trigger专用fm107.8
        print "\033[43;1m going to send alert msg...........\033[0m"
        print "trigger_notifier argv:",host_obj,trigger_id,positive_expressions

        msg_dic = {'host_id': host_obj.id,
                   'trigger_id': trigger_id,
                   'positive_expressions': positive_expressions,
                   'msg': msg,
                   'time': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                   'start_time': time.time(),
                   'duration': None,    #持续时间
                   }
        '''eg: {'positive_expressions': [{'calc_res': True, 'calc_res_val': 50.0, 'expression_obj': 11L, 'service_item': None}],
                'start_time': 1479746290.294948,
                'trigger_id': 4L,
                'duration': None,
                'time': '2016-11-21 16:38:10',
                'msg': u'linux_memory_critical',
                'host_id': 7L}
        '''
        self.redis2.public(pickle.dumps(msg_dic))

        #先把之前的trigger加载回来，获取上次报警的时间，以统计故障持续时间
        trigger_redis_key = "host_%s_trigger_%s" %(host_obj.id,trigger_id)
        old_trigger_data = self.redis2.get(trigger_redis_key)
        if old_trigger_data:
            trigger_startime = json.loads(old_trigger_data)['start_time']
            msg_dic['start_time'] = trigger_startime
            msg_dic['duration'] = round(time.time() - trigger_startime)
        #同时在redis中记录这个trigger，前端页面展示时要 统计trigger个数
        self.redis2.set_300(trigger_redis_key,json.dumps(msg_dic),300)  #一个trigger记录5分钟后自动清除（过期）


class ExpressionProcess(object):    #load data and calc it by different method
    def __init__(self,main_ins,host_obj,expression_obj,specified_item=None):
        '''
        :param main_ins: DataHandler实例
        :param host_obj:
        :param expression_obj
        :return 计算表达式的结果
        '''
        self.host_obj = host_obj
        self.expression_obj = expression_obj
        self.main_ins = main_ins
        self.service_redis_key = "StatusData_%s_%s_latest" %(host_obj.id,expression_obj.service.name) #拼出此服务在redis中的key
        self.time_range = self.expression_obj.data_calc_args.split(',')[0]  #获取要从redis中取多长时间的数据，单位是min
        print "\033[31;1m------>%s\033[0m" %self.service_redis_key

    def process(self):
        data = self.load_data_from_redis()  #按照配置把数据从redis里取出来，比如最近2分钟，或10分钟的数据
        data_calc_func = getattr(self,'get_%s' %self.expression_obj.data_calc_func) #eg:('avg','Average'),('max','Max'),('hit','Hit'),('last','Last'),
        single_expression_calc_res = data_calc_func(data)   #计算。。。
        print "---res of single_expression_calc_res ",single_expression_calc_res
        if single_expression_calc_res:  #确保上面的条件有正确的返回
            res_dic = {
                'calc_res': single_expression_calc_res[0],
                'calc_res_val': single_expression_calc_res[1],
                'expression_obj': self.expression_obj,
                'service_item': single_expression_calc_res[2]
            }
            return res_dic
        else:
            return False

    def get_avg(self,data_set):
        clean_data_list = []
        clean_data_dic = {}
        for point in data_set:
            val,saving_time = point
            #print "---point:>", val
            if val:
                if 'data' not in val: #没有子dict
                    clean_data_list.append(val[self.expression_obj.service_index.key])
                else:   #has sub dict
                    for k,v in val['data'].items():
                        if k not in clean_data_dic:
                            clean_data_dic[k] = []
                        clean_data_dic[k].append(val[self.expression_obj.service_index.key])

        if clean_data_list:
            clean_data_list = [float(i) for i in clean_data_list]
            avg_res = sum(clean_data_list) / len(clean_data_list)
            #print "\033[46;1m----avg res:%s\033[0m" %avg_res
            print clean_data_list
            return [self.judge(avg_res),avg_res,None]
        elif clean_data_dic:
            pass
        else:       #未取得汇报数据的情况
            return [False,None,None]

    def judge(self,calculated_val):
        '''
        :param calculated_val   #已经算好的结果,eg: avg(2)
        :return
        '''
        calc_func = getattr(operator,self.expression_obj.operator_type)     #根据对应运算符，调用python处理方式，返回true或false
        return calc_func(calculated_val,self.expression_obj.threshold)  #其中threshold是设置的阀值

    def get_hit(self,data_set):
        pass

    def load_data_from_redis(self):
        #load data from redis according to expression's configuration
        time_in_sec = int(self.time_range) * 60     #下面的+60是默认多取1分钟数据，多出来的后面会去掉
        approximate_data_points = (time_in_sec + 60) / self.expression_obj.service.interval #用额外参数时间+60秒，除以监控间隔，获取一个大概要取的值
        print "approximate dataset nums:",approximate_data_points,time_in_sec
        data_range_raw = self.main_ins.redis.lrange(self.service_redis_key,-approximate_data_points,-1)
        #print "\033[31;1m------>%s\033[0m" %data_range_raw
        approximate_data_range = [json.loads(i) for i in data_range_raw]
        data_range = []     #精确的需要的数据列表
        for point in approximate_data_range:
            var,saving_time = point
            if time.time() - saving_time < time_in_sec: #代表没有超时上报，数据有效
                data_range.append(point)
        #print data_range
        return data_range


if __name__ == '__main__':
    reactor = DataHandler(redis)
    reactor.looping()