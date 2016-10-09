#coding:utf-8
__author__ = 'Administrator'
import time
import json
import paramiko
from hosts import models
from django.utils import timezone   #导入django的时间
from s10ops import settings

def paramiko_ssh(task_id, host_obj, task_content):
    print "going to run: ",host_obj,task_content
    bind_host = host_obj
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if bind_host.host_user.auth_type == 'ssh-password':
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      bind_host.host_user.password,
                      timeout=5)
        else:#rsa_key
            pass
            '''
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      pkey=key,
                      timeout=5)
            '''
        stdin,stdout,stderr = s.exec_command(task_content)
        result = stdout.read(),stderr.read()
        cmd_result = filter(lambda x:len(x)>0, result)[0]
        result = 'success'
    except Exception,e:
        print("\033[31;1m%s\033[0m" % e)
        cmd_result = e
        result = 'failed'
    #for line in cmd_result:
    #    print line

    #save output into db 根据已创建的task_id修改覆盖
    log_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id,bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result

    log_obj.save()

def paramiko_sftp(task_id,host_obj,task_content,task_type,user_id):
    bind_host = host_obj
    try:
        t = paramiko.Transport((bind_host.host.ip_addr,int(bind_host.host.port)))
        if bind_host.host_user.auth_type == 'ssh-password':
            t.connect(username=bind_host.host_user.username,password=bind_host.host_user.password)
        else:
            pass
            #key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            #t.connect(username=bind_host.host_user.username,pkey=key)
        sftp = paramiko.SFTPClient.from_transport(t)

        task_dic = json.loads(task_content)

        if task_type == 'file_send':
            upload_files = task_dic['upload_files']
            #print upload_files
            for file_path in upload_files:
                file_abs_path = "%s\%s\%s" %(settings.FileUploadDir,user_id,file_path)
                #print file_abs_path
                remote_filename = file_path.split("\\")[-1]
                print "---\033[32;1m sending [%s] to [%s]\033[0m" %(remote_filename,task_dic['remote_path'])
                sftp.put(file_abs_path, "%s/%s"%(task_dic['remote_path'],remote_filename))
            cmd_result = "successfully send files %s to remote path [ %s ]" %(upload_files,task_dic['remote_path'])
            result = 'success'
        else:
            pass
    except Exception,e:
        print e
        cmd_result = e
        result = 'failed'
    log_obj= models.TaskLogDetail.objects.get(child_of_task_id=task_id,bind_host_id=bind_host.id)
    log_obj.event_log = cmd_result
    log_obj.date = timezone.now()
    log_obj.result = result

    log_obj.save()

