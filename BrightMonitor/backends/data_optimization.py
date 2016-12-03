#coding:utf-8
__author__ = 'xuefeng'

import time,json
import copy
from BrightMonitor import settings
from redis_conn import RedisHelper as redis

class DataStore(object):
    def __init__(self,client_id,service_name,data):
        self.redis = redis()
        self.client_id = client_id
        self.service_name = service_name
        self.data = data
        self.process_and_save()

    def get_data_slice(self,latest_data_key,optimization_interval):
        '''
        :param optimization_interval: eg: 600, means get latest 10 mins real data from redis
        :return
        '''
        all_real_data = self.redis.lrange(latest_data_key,-1,-1)
        #print "get data range of:",latest_data_key,optimization_interval
        #print "get data range of:",all_real_data[-1]
        data_set = []
        for item in all_real_data:
            data = json.loads(item)
            if len(data) == 2:
                #print "real data item:",data[0],data[1]
                service_data,last_save_time = data
                if time.time() - last_save_time <= optimization_interval:   #filter this data point out
                    data_set.append(data)
                else:
                    pass
        return data_set

    def process_and_save(self):
        #processing data and save into redis
        print "\033[42;1m----service data------------\033[0m"
        #print self.client_id,self.service_name,self.data
        if self.data['status'] == 0:    #service data is valid

            uptime_in_redis_key = 'StatusData_%s_uptime_latest' %self.client_id
            ######################################
            ######################################
            ######################################

            for key,data_series_val in settings.STATUS_DATA_OPTIMIZATION.items():
                data_series_key_in_redis = "StatusData_%s_%s_%s" %(self.client_id,self.service_name,key)
                #print data_series_key_in_redis,data_series_val
                last_point_from_redis = self.redis.lrange(data_series_key_in_redis,-1,-1)
                if not last_point_from_redis:
                    self.redis.rpush(data_series_key_in_redis,json.dumps([None,time.time()]))
                if data_series_val[0] == 0:     #latest data,eg: StatusData_7_linux_cpu_latest [0, 600]
                    self.redis.rpush(data_series_key_in_redis,json.dumps([self.data,time.time()]))
                else:
                    last_point_data,last_point_save_time = json.loads(self.redis.lrange(data_series_key_in_redis,-1,-1)[0])
                    if time.time() - last_point_save_time >= data_series_val[0]:    #reached the data point updata interval
                        latest_data_key_in_redis = "StatusData_%s_%s_latest" %(self.client_id,self.service_name)
                        print "calulating data for key:\033[31;1m%s\033[0m" %data_series_key_in_redis

                        #最近n分钟的数据已经取到了，放到data_set里
                        data_set = self.get_data_slice(latest_data_key_in_redis,data_series_val[0])
                        print "---------------------------len dataset: ",len(data_set)

                        if len(data_set) > 0:
                            #把data_set交给下面这个方法，算出优化的结果来
                            optimized_data = self.get_optimized_data(data_series_key_in_redis,data_set)
                            if optimized_data:
                                self.save_optimized_data(data_series_key_in_redis,optimized_data)
                #同时确保数据在redis中存储数量不超过settings中指定的值
                if self.redis.llen(data_series_key_in_redis) >= data_series_val[1]:
                    self.redis.lpop(data_series_key_in_redis)   #删除最旧一个数据
        else:
            print "report data is invalid::",self.data
            raise ValueError

    def save_optimized_data(self,data_series_key_in_redis,optimized_data):
        self.redis.rpush(data_series_key_in_redis,json.dumps([optimized_data, time.time()]))

    def get_optimized_data(self,data_set_key,raw_service_data):
        '''
        :param data_set_key: where the optimized data needed to save to in redis db
        :param raw_service_data: raw service data datalist
        :return
        '''
        print "get_optimized_data:",raw_service_data[0]
        service_data_keys = raw_service_data[0][0].keys()   #eg: iowait, idle, system...
        first_service_data_point = raw_service_data[0][0]   #用来创建一个新dict
        #print "--->",service_data_keys
        optimized_dic = {}  #will save optimized data later
        if 'data' not in service_data_keys: #表示cpu,memory等的上报数据
            for key in service_data_keys:
                optimized_dic[key] = []
            tmp_data_dic = copy.deepcopy(optimized_dic)     #临时存最近n分钟的数据，按指标搞成一个个列表
            #print "tmp data dic:",tmp_data_dic
            for service_data_item,last_save_time in raw_service_data:   #loop最近n分钟的数据
                #print service_data_item
                for service_index,v in service_data_item.items():   #loop每个数据记录点的数据
                    try:
                        tmp_data_dic[service_index].append(round(float(v),2))   #把这个点的当前这个指标的值添加到临时dict中
                    except ValueError,e:
                        pass
                #print service_data_item,last_save_time

            for service_k,v_list in tmp_data_dic.items():
                #print service_k,v_list
                avg_res = self.get_average(v_list)
                max_res = self.get_max(v_list)
                min_res = self.get_min(v_list)
                mid_res = self.get_mid(v_list)
                optimized_dic[service_k] = [avg_res,max_res,min_res,mid_res]
                print service_k, optimized_dic[service_k]

        else:   #处理有子服务的上报数据，即：has sub dic inside key 'data'
            pass
            ##################################
            #################################

        return optimized_dic

    def get_average(self,data_set):
        if len(data_set) > 0:
            return sum(data_set) / len(data_set)
        else:
            return 0
    def get_max(self,data_set):
        if len(data_set) > 0:
            return max(data_set)
        else:
            return 0
    def get_min(self,data_set):
        if len(data_set) > 0:
            return min(data_set)
        else:
            return 0
    def get_mid(self,data_set):
        if len(data_set) > 0:
            data_set.sort() #先排序
            return data_set[len(data_set)/2]
        else:
            return 0