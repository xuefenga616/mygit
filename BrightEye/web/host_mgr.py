#coding:utf-8
__author__ = 'Administrator'

import models,json,subprocess
import paramiko,time,os,re
import multiprocessing
from BrightEye import settings
from django.db import transaction
from backend.utils import json_date_handle
import yaml

class MultiTask(object):
    def __init__(self,task_type,request_ins):
        self.request = request_ins
        self.task_type = task_type
    def run(self):
        task_func = getattr(self,self.task_type)
        return task_func()

    def run_cmd(self):
        cmd = self.request.POST.get('cmd')
        selected_hosts = json.loads(self.request.POST.get('selected_hosts'))
        host_ids = [int(i.split('host_')[-1]) for i in selected_hosts]
        expire_time = self.request.POST.get('expire_time')
        exec_hosts = models.BindHosts.objects.filter(id__in=host_ids) #eg:[<BindHosts: lvs-01:root>, <BindHosts: lvs-02:root>]

        task_obj = self.create_task_log('cmd',exec_hosts,expire_time,cmd)
        #subprocess.Popen()跑任务脚本
        p = subprocess.Popen(['python',
                              settings.MultiTaskScript,
                              '-task_type','cmd',
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-task',cmd,
                              '-task_id',str(task_obj.id)])

        return task_obj.id

    def file_get(self):     #下载文件
        return self.file_send()

    def file_send(self):
        params = json.loads(self.request.POST.get('params'))
        host_ids = [int(i.split('host_')[-1]) for i in params.get('selected_hosts')]
        expire_time = params.get('expire_time')
        exec_hosts = models.BindHosts.objects.filter(id__in=host_ids)   #从数据库中取出要执行任务的主机
        task_type = self.request.POST.get('task_type')
        local_file_list = params.get('local_file_list')
        remote_file_path = params.get('remote_file_path')
        if task_type == 'file_send':
            content = "send local files %s to remote path [%s]" %(local_file_list,params.get('remote_file_path'))
        else:
            local_file_list = 'not_required'    #防止混乱出错
            content = 'download remote file [%s]' %params.get('remote_file_path')

        task_obj = self.create_task_log(task_type,exec_hosts,expire_time,content)
        if task_type == 'file_get':
            local_path = "%s\\%s\\%s" %(settings.BASE_DIR,settings.FileUploadDir,self.request.user.userprofile.id)
            if not os.path.isdir(local_path):
                os.mkdir(local_path)

        p = subprocess.Popen(['python',
                              settings.MultiTaskScript,
                              '-task_type',task_type,
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-local',' '.join(local_file_list),
                              '-remote',remote_file_path,
                              '-task_id',str(task_obj.id)])

        task_obj.save()
        return task_obj.id

    def bigtask(self):
        params = json.loads(self.request.POST.get('params'))
        host_ids = [int(i.split('host_')[-1]) for i in params.get('selected_hosts')]
        expire_time = params.get('expire_time')
        exec_hosts = models.BindHosts.objects.filter(id__in=host_ids)   #从数据库中取出要执行任务的主机
        # task_type = self.request.POST.get('task_type')
        task_type = "file_send"
        local_file_list = params.get('local_file_list')
        remote_file_path = params.get('remote_file_path')

        content = "bigtask: send packages %s to remote path [%s]" %(local_file_list,params.get('remote_file_path'))
        task_obj = self.create_task_log(task_type,exec_hosts,expire_time,content)
        local_path = "%s\\%s\\%s" %(settings.BASE_DIR,settings.FileUploadDir,self.request.user.userprofile.id)
        if not os.path.isdir(local_path):
            os.mkdir(local_path)

        task_obj.save()
        ############################
        #拷贝部署包到客户机并解包
        p_send = subprocess.Popen(['python',
                              settings.GigTaskScript,
                              '-task_type',"file_send",
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-local',' '.join(local_file_list),
                              '-remote',"/tmp",
                              '-task_id',str(task_obj.id)])
        zip_packages = [i for i in local_file_list if re.search(r".zip$",i)][0]
        remote_zip_packages = "/tmp/" + zip_packages.split('\\')[-1]
        if remote_zip_packages is not None:
            #print remote_zip_packages
            p_unzip = subprocess.Popen(['python',
                              settings.GigTaskScript,
                              '-task_type','cmd',
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-task',"unzip %s -d /tmp"%remote_zip_packages,
                              '-task_id',str(task_obj.id)])
            task_dir = remote_zip_packages.split(".zip")[:-1]
            print task_dir
        ############################
        yaml_file = [i for i in local_file_list if re.search(r".yaml$",i)][0]
        conf_dic = yaml.load(file(yaml_file,'r'))
        #print conf_dic
        cmd = conf_dic['cmd']
        p_run = subprocess.Popen(['python',
                              settings.GigTaskScript,
                              '-task_type','cmd',
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-task',cmd,
                              '-task_id',str(task_obj.id)])
        if conf_dic['file_get'] is not None:
            fileget_ip_addr = conf_dic['file_get'][0]['ip_addr']
            fileget_host = models.BindHosts.objects.get(host__ip_addr=fileget_ip_addr)
            #print fileget_host
            fileget_filename = conf_dic['file_get'][1]['filename']
            fileget_filename_gen = fileget_filename + "_" + fileget_ip_addr
            p_get1 = subprocess.Popen(['python',
                              settings.GigTaskScript,
                              '-task_type',"file_get",
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-local','not_required',
                              '-remote',fileget_filename,
                              '-task_id',str(task_obj.id)])

            if conf_dic['file_send'] is not None:
                filesend_ip_addr = conf_dic['file_send'][0]['ip_addr']
                filesend_host = models.BindHosts.objects.get(host__ip_addr=filesend_ip_addr)
                #print filesend_host
                #local_file_list = local_file_list[0].split('\\')[:-1] + '\\' + conf_dic['file_get'][1]['filename'].split('/')[:-1] + "_" + conf_dic['file_get'][0]['ip_addr']
                #print local_file_list
                #filesend_filename = '\\' + conf_dic['file_get'][1]['filename'].split('/')[:-1] + "_" + conf_dic['file_get'][0]['ip_addr']
                #print filesend_filename
                # p_send1 = subprocess.Popen(['python',
                #                   settings.MultiTaskScript,
                #                   '-task_type',"file_send",
                #                   '-expire',expire_time,
                #                   '-uid',str(self.request.user.userprofile.id),
                #                   '-local',filesend_filename,
                #                   '-remote',conf_dic['file_send'][1]['filename'],
                #                   '-task_id',str(task_obj.id)])
            if conf_dic['cmd2'] is not None:
                cmd2 = conf_dic['cmd2']

        return task_obj.id

    @transaction.atomic     #函数从头执行到尾不中断
    def create_task_log(self,task_type,hosts,expire_time,content,note=None):
        task_log_obj = models.TaskLog(
            task_type = task_type,
            user = self.request.user.userprofile,
            cmd = content,
            expire_time = int(expire_time),
            note = note
        )
        task_log_obj.save()
        task_log_obj.hosts.add(*hosts)
        #init detail logs
        for h in hosts:
            task_log_detail_obj = models.TaskLogDetail(
                child_of_task_id = task_log_obj.id,
                bind_host_id = h.id,
                event_log = '',
                result = 'unknown'
            )
            task_log_detail_obj.save()
        return task_log_obj

    def get_task_result(self,detail=True):
        task_id = self.request.GET.get('task_id')
        log_dic = {
            'detail':{}
        }
        task_obj = models.TaskLog.objects.get(id=int(task_id))
        task_detail_obj_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_obj.id)
        log_dic['summary'] = {
            'id': task_obj.id,
            'start_time': task_obj.start_time,
            'end_time': task_obj.end_time,
            'task_type': task_obj.task_type,
            'host_num': task_obj.hosts.select_related().count(),
            'finished_num': task_detail_obj_list.filter(result='success').count(),
            'failed_num': task_detail_obj_list.filter(result='failed').count(),
            'unknown_num': task_detail_obj_list.filter(result='unknown').count(),
            'content': task_obj.cmd,
            'expire_time': task_obj.expire_time
        }

        if detail:
            for log in task_detail_obj_list:
                log_dic['detail'][log.id] = {
                    'date': log.date,
                    'bind_host_id': log.bind_host_id,
                    'host_id': log.bind_host.host.id,
                    'hostname': log.bind_host.host.hostname,
                    'ip_addr': log.bind_host.host.ip_addr,
                    'username': log.bind_host.host_user.username,
                    'system': log.bind_host.host.system_type,
                    'event_log': log.event_log,
                    'result': log.result,
                    'note': log.note
                }
        return json.dumps(log_dic,default=json_date_handle) #json_date_handler用来将日期转化为字符串