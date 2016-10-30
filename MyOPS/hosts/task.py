#coding:utf-8
__author__ = 'Administrator'
import models
from django.db import transaction
import subprocess   #类似commands
from MyOPS import settings  #引入脚本的全局变量MultiTaskScript
import json

class Task(object):
    def __init__(self,request):
        self.request = request
        self.task_type = self.request.POST.get("task_type")
    def handle(self):   #根据任务类型返回方法
        if self.task_type:
            if hasattr(self,self.task_type):
                func = getattr(self, self.task_type)
                return func()
            else:
                raise TypeError
    @transaction.atomic     #此装饰器的作用是：等函数执行完毕后，才commit一次
    def multi_cmd(self):
        print "---going to run cmd---"
        print self.request.POST
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        cmd = self.request.POST.get("cmd")
        print '--->',selected_hosts,cmd
        #create task info
        task_obj = models.TaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            #many to many必须在创建完记录后再添加
            cmd = cmd,
        ) #开始写入数据库
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) #添加m2m

        #create task detail record for all the hosts will be exec
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A",
            )
            obj.save()

        #返回前调脚本 invoke backend multi_task.py script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id',str(task_obj.id),
            '-run_type',settings.MultiTaskRunType,
        ])

        return {'task_id': task_obj.id}     #返回任务id

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id: #去数据库里获取
            res_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
            #把数据库里的数据转化为字典：res_list.values()，再转化为列表，再dumps()
            return list(res_list.values('id',
                                        'bind_host__host__hostname',
                                        'bind_host__host__ip_addr',
                                        'bind_host__host_user__username',
                                        'date',
                                        'event_log',
                                        'result',
                                        ))  #指定显示的内容

    def multi_file_transfer(self):
        print "----going to handle file uploading/download"
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        transfer_type = self.request.POST.get('file_transfer_type')
        remote_path = self.request.POST.get('remote_path')
        upload_files = self.request.POST.getlist('upload_files[]')

        #create task info
        data_dic = {
            'remote_path':remote_path,
            'upload_files':upload_files,
        }
        task_obj = models.TaskLog(
            task_type = transfer_type,
            user_id = self.request.user.id,
            #many to many必须在创建完记录后再添加
            cmd = json.dumps(data_dic),
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) #添加m2m关系
        #create task detail record for all the hosts will be executed later
        for bind_host_id in selected_hosts:
            obj =models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A",
            )
            obj.save()

        #invoke backend multitask script
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id',str(task_obj.id),
            '-run_type',settings.MultiTaskRunType,
        ])

        return {'task_id': task_obj.id}     #返回任务id