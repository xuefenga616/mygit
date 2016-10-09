#coding:utf-8
from django.db import models

# Create your models here.
from myauth import UserProfile
class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    system_type_choices = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
    )
    system_type = models.CharField(choices=system_type_choices, max_length=32,default='linux')
    idc = models.ForeignKey('IDC')
    enabled = models.BooleanField(default=True)
    memo = models.TextField(blank=True, null=True)  #备注
    date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s(%s)" %(self.hostname, self.ip_addr)
    class Meta:
        verbose_name = u'主机列表'
        verbose_name_plural = u"主机列表"

class IDC(models.Model):
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.name

class HostUser(models.Model):   #远程用户
    auth_type_choices = (
        ('ssh-password', 'SSH/Password'),
        ('ssh-key', 'SSH/KEY'),
    )
    auth_type = models.CharField(choices=auth_type_choices, max_length=32, default='ssh-password')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)
    def __unicode__(self):
        return "(%s)%s" %(self.auth_type, self.username)
    class Meta:     #保持账号唯一性
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = u'远程主机用户'
        verbose_name_plural = u"远程主机用户"

class HostGroup(models.Model):  #主机组
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u"主机组"

class BindHostToUser(models.Model): #绑定关系
    host = models.ForeignKey('Host')
    host_user = models.ForeignKey('HostUser')
    #host_user = models.ManyToManyField("HostUser")
    host_groups = models.ManyToManyField("HostGroup")
    class Meta:     #保持创建主机、用户唯一性
        unique_together = ('host', 'host_user')
        verbose_name = u'主机与用户绑定关系'
        verbose_name_plural = u"主机与用户绑定关系"
    def __unicode__(self):
        return "%s:%s" %(self.host.hostname, self.host_user.username)
    def get_groups(self):   #可以显示多对多的函数
        return ','.join([g.name for g in self.host_groups.select_related()])

class TaskLog(models.Model):    #任务信息表
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)
    task_type_choices = (('multi_cmd',"CMD"),('file_send',"批量发送文件"),('file_get',"批量下载文件"))
    task_type = models.CharField(choices=task_type_choices,max_length=50)
    user = models.ForeignKey('UserProfile')
    hosts = models.ManyToManyField('BindHostToUser')
    cmd = models.TextField()
    expire_time = models.IntegerField(default=30)   #超时时间
    task_pid = models.IntegerField(default=0)
    note = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return "taskid:%s cmd:%s" %(self.id,self.cmd)
    class Meta:
        verbose_name = u'批量任务'
        verbose_name_plural = u'批量任务'

class TaskLogDetail(models.Model):  #任务返回结果表
    child_of_task = models.ForeignKey('TaskLog')
    bind_host  = models.ForeignKey('BindHostToUser')
    date = models.DateTimeField(auto_now_add=True) #finished date
    event_log = models.TextField()
    result_choices= (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices,max_length=30,default='unknown')
    note = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return "child of:%s result:%s" %(self.child_of_task.id, self.result)
    class Meta:
        verbose_name = u'批量任务日志'
        verbose_name_plural = u'批量任务日志'


