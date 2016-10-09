#coding:utf-8
import models
from django.db import transaction
import subprocess,os,json
from s10ops import settings

__author__ = 'Administrator'
class Task(object):
    def __init__(self, request):
        self.request = request
        self.task_type = self.request.POST.get('task_type')
    def handle(self):
        if self.task_type:
            if hasattr(self, self.task_type):
                func = getattr(self,self.task_type)
                return func()
            else:
                raise TypeError
    @transaction.atomic     #此装饰器作用：等函数执行完，才commit
    def multi_cmd(self):
        print "---going to run cmd---"
        print self.request.POST
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        print selected_hosts
        cmd = self.request.POST.get("cmd")
        #create task info
        task_obj = models.TaskLog(
            task_type = self.task_type,
            user_id = self.request.user.id,
            #manyToMany必须在创建完记录后再添加
            cmd = cmd,
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) #添加m2m关系！传列表方法
        #create task detail record fro all the hosts will be executed
        for bind_host_id in selected_hosts:
            obj = models.TaskLogDetail(
                child_of_task_id = task_obj.id,
                bind_host_id = bind_host_id,
                event_log = "N/A",
            )
            obj.save()

        #invoke backend multitask script 调用脚本
        p = subprocess.Popen([
            'python',
            settings.MultiTaskScript,
            '-task_id',str(task_obj.id),
            '-run_type',settings.MultiTaskRunType,
        ],) #preexec_fn=os.setsid)
        #print "---->pid:", p.pid
        return {'task_id': task_obj.id}

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
            return list(res_list.values('id',
                                        'bind_host__host__hostname',
                                        'bind_host__host__ip_addr',
                                        'bind_host__host_user__username',
                                        'date',
                                        'event_log',
                                        'result',
                                        ))

    def multi_file_transfer(self):
        print '----going to handle file uploading/download'
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        transfer_type = self.request.POST.get("file_transfer_type")
        remote_path = self.request.POST.get("remote_path")
        upload_files = self.request.POST.getlist("upload_files[]")
        #create task info
        data_dic = {
            'remote_path':remote_path,
            'upload_files':upload_files,
        }
        task_obj = models.TaskLog(
            task_type = transfer_type,
            user_id = self.request.user.id,
            #manyto many 必须 在创建完纪录后再添加
            cmd = json.dumps(data_dic),
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts) #添加m2m关系
        #task_obj.hosts.add([1,2,3])

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
        ])# ,preexec_fn=os.setsid)
        #print '----->pid:',p.pid

        return {'task_id': task_obj.id}


