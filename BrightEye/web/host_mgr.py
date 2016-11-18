#coding:utf-8
__author__ = 'Administrator'

import models,json,subprocess
import paramiko,time,os,re
import multiprocessing
from BrightEye import settings
from django.db import transaction
from backend.utils import json_date_handle
import yaml
from backend import multitask

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
        task_type = self.request.POST.get('task_type')
        local_file_list = params.get('local_file_list')
        remote_file_path = params.get('remote_file_path')

        content = ""
        local_path = "%s\\%s\\%s" %(settings.BASE_DIR,settings.FileUploadDir,self.request.user.userprofile.id)
        if not os.path.isdir(local_path):
            os.mkdir(local_path)

        ############################
        #拷贝部署包到客户机并解包
        yaml_file = [i for i in local_file_list if re.search(r".yaml$",i)][0]
        content = yaml.load(file(yaml_file,'r'))
        content = json.dumps(content)
        task_obj = self.create_task_log(task_type,exec_hosts,expire_time,content)
        p = subprocess.Popen(['python',
                              settings.BigTaskScript,
                              '-task_type',task_type,
                              '-expire',expire_time,
                              '-uid',str(self.request.user.userprofile.id),
                              '-local',' '.join(local_file_list),
                              '-conf',content,
                              '-remote',remote_file_path,
                              '-task_id',str(task_obj.id)])
        ############################

        task_obj.save()
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

class Bigtask_exec(object):
    def __init__(self,task_type,local_path,**conf_dic):
        self.request = conf_dic
        self.task_type = task_type
        self.local_path = local_path
    def run(self):
        task_func = getattr(self,self.task_type)
        return task_func()
    def bigtask_exec(self):
        conf_dic = self.request
        local_path = self.local_path

        if conf_dic['master'] is not None:
            m_conf_list = conf_dic['master']
            m_ip_addr = m_conf_list[0]['ip_addr']
            m_cmd = m_conf_list[1]['cmd']
            ##########################################
            #开始处理第一组命令
            m_host = models.BindHosts.objects.get(host__ip_addr=m_ip_addr)   #从数据库中取出要执行任务的主机
            print "master host is %s" %m_host
            cmd_result = multitask.cmd_paramiko(m_host.id,m_cmd)
            #print cmd_result
            ##########################################
            m_get_file = m_conf_list[2]['file_get']
            m_cmd2 = m_conf_list[3]['cmd2']
            if conf_dic['slave1'] is not None:
                s_conf_list = conf_dic['slave1']
                s_ip_addr = s_conf_list[0]['ip_addr']
                s_cmd = s_conf_list[1]['cmd']
                ##########################################
                #开始处理第二组命令
                s_host = models.BindHosts.objects.get(host__ip_addr=s_ip_addr)   #从数据库中取出要执行任务的主机
                print "slave1 host is %s" %s_host
                cmd_result += multitask.cmd_paramiko(s_host.id,s_cmd)
                print cmd_result
                ##########################################
                if m_get_file is not None:
                    s_send_file = s_conf_list[2]['file_send']
                    s_cmd2 = s_conf_list[3]['cmd2']
                    ##########################################
                    #开始处理第三组命令

                    ##########################################
        print """
            m_ip_addr is: %s,
            m_cmd is: %s,
            m_get_file is: %s,
            m_cmd2 is: %s,
            ***********************
            s_ip_addr is: %s,
            s_cmd is: %s,
            s_send_file is: %s,
            s_cmd2 is: %s,
        """ %(m_ip_addr,m_cmd,m_get_file,m_cmd2,s_ip_addr,s_cmd,s_send_file,s_cmd2)






