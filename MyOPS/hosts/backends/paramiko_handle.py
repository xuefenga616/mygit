#coding:utf-8
__author__ = 'Administrator'
import paramiko,json
from hosts import models
from django.utils import timezone
from MyOPS import settings

def paramiko_ssh(task_id,host_obj,task_content):
    print 'going to run --->:',host_obj,task_content
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
        else:   #rsa_key
            pass
        stdin,stdout,stderr = s.exec_command(task_content)
        result = stdout.read(),stderr.read()
        cmd_result = filter(lambda x:len(x)>0,result)[0]
        result = 'success'
    except Exception,e:
        print "\033[31;1m %s\033[0m" %e
        cmd_result = e
        result = 'failed'

    #for line in cmd_result:
    #    print line,

    #执行结果写到数据库，是修改，不是创建
    log_obj = models.TaskLogDetail.objects.get(child_of_task_id = task_id,bind_host_id = bind_host.id)
    log_obj.date = timezone.now()  #开始修改数据库，先取django的当前时间
    log_obj.event_log = cmd_result
    log_obj.result = result
    log_obj.save()

def paramiko_sftp(task_id,host_obj,task_content,task_type,user_id):
    bind_host = host_obj

    try:
        t = paramiko.Transport((bind_host.host.ip_addr,int(bind_host.host.port) ))
        if bind_host.host_user.auth_type == 'ssh-password':

            t.connect(username=bind_host.host_user.username,password=bind_host.host_user.password)
        else:
            pass

            #key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            #t.connect(username=bind_host.host_user.username,pkey=key)
        sftp = paramiko.SFTPClient.from_transport(t)

        task_dic = json.loads(task_content)     #把数据库里的任务详情取出来
        if task_type == 'file_send':
            upload_files = task_dic['upload_files']
            for file_path in upload_files:
                file_abs_path = "%s\\%s\\%s" %(settings.FileUploadDir,user_id,file_path)
                #print file_abs_path
                remote_filename = file_path.split("\\")[-1]
                print '---\033[32;1m sending [%s] to [%s]\033[0m' %(remote_filename,task_dic['remote_path'])
                #下面是真正传文件
                sftp.put(file_abs_path,"%s/%s" %(task_dic['remote_path'],remote_filename))
            cmd_result = "successfully send files %s to remote path [%s]" %(upload_files,task_dic['remote_path'])
            result = 'success'
        else:
            pass

    except Exception,e:
        print e
        cmd_result = e
        result = 'failed'

    #执行结果写到数据库，是修改，不是创建
    log_obj = models.TaskLogDetail.objects.get(child_of_task_id = task_id,bind_host_id = bind_host.id)
    log_obj.date = timezone.now()  #开始修改数据库，先取django的当前时间
    log_obj.event_log = cmd_result
    log_obj.result = result
    log_obj.save()
