#coding:utf-8
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)
    def __unicode__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=64,unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'部门'
        verbose_name_plural = u'部门'

class Hosts(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    system_type_choices = (
        ('windows','Windows'),
        ('linux','Linux')
    )
    system_type = models.CharField(choices=system_type_choices,max_length=32,default='linux')
    idc = models.ForeignKey('IDC')
    port = models.IntegerField(default=22)
    enabled = models.BooleanField(default=True)     #是否生效、可见
    memo = models.CharField(max_length=128,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s(%s)' %(self.hostname,self.ip_addr)
    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u'主机'

class HostUsers(models.Model):
    auth_method_choices = (
        ('ssh-password',"SSH/Password"),
        ('ssh-key',"SSH/KEY")
    )
    auth_method = models.CharField(choices=auth_method_choices,max_length=16,help_text=u'如果选择SSH/KEY，请确保私钥文件已在settings.py中指定')
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64,blank=True,null=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return "(%s)%s" %(self.auth_method,self.username)
    class Meta:
        verbose_name = u'远程主机用户'
        verbose_name_plural = u'远程主机用户'
        unique_together = ('auth_method','username','password')

class HostGroups(models.Model):
    name = models.CharField(max_length=64,unique=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u'主机组'

class BindHosts(models.Model):
    host = models.ForeignKey('Hosts')
    host_user = models.ForeignKey('HostUsers')
    host_group = models.ManyToManyField('HostGroups')
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s:%s' %(self.host.hostname,self.host_user.username)
    class Meta:
        verbose_name = u'主机与远程用户绑定'
        verbose_name_plural = u'主机与远程用户绑定'
        unique_together = ('host','host_user')
    def get_groups(self):
        return ',\n'.join([g.name for g in self.host_group.all()])

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32,unique=True)
    department = models.ForeignKey('Department',verbose_name=u'部门')
    host_groups = models.ManyToManyField('HostGroups',blank=True,verbose_name=u'授权主机组')
    bind_hosts = models.ManyToManyField('BindHosts',blank=True,verbose_name=u'授权主机')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'BrightEye账户'
        verbose_name_plural = u'BrightEye账户'

class AuditLog(models.Model):
    user = models.ForeignKey('UserProfile')
    host = models.ForeignKey('BindHosts')
    action_choices = (
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'exception'),
    )
    action_type = models.IntegerField(choices=action_choices,default=0)
    cmd = models.TextField()
    memo = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateTimeField()
    def __unicode__(self):
        return '%s-->%s@%s:%s' %(self.user.user.username,self.host.host_user.username,self.host.host.ip_addr,self.cmd)
    class Meta:
        verbose_name = u'审计日志'
        verbose_name_plural = u'审计日志'

class TaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True,null=True)
    task_type_choices = (
        ('cmd',"CMD"),
        ('file_send',u'批量发送文件'),
        ('file_get',u'批量下载文件'),
        ('bigtask',u'计划任务')
    )
    task_type = models.CharField(choices=task_type_choices,max_length=64)
    user = models.ForeignKey('UserProfile')
    hosts = models.ManyToManyField('BindHosts')
    cmd = models.TextField()
    expire_time = models.IntegerField(default=30)
    task_pid = models.IntegerField(default=0)
    note = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return 'taskid:%s cmd:%s' %(self.id,self.cmd)
    class Meta:
        verbose_name = u'批量任务'
        verbose_name_plural = u'批量任务'

class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('TaskLog')
    bind_host = models.ForeignKey('BindHosts')
    date = models.DateTimeField(auto_now_add=True)  #finished time
    event_log = models.TextField()
    result_choices = (
        ('success','Success'),
        ('filed','Failed'),
        ('unknown','Unknown')
    )
    result = models.CharField(choices=result_choices,max_length=32,default='unknown')
    note = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return 'child of:%s result:%s' %(self.child_of_task.id,self.result)
    class Meta:
        verbose_name = u'批量任务日志'
        verbose_name_plural = u'批量任务日志'

class Token(models.Model):  #防止重复提交
    user = models.ForeignKey(UserProfile)
    host = models.ForeignKey(BindHosts)
    token = models.CharField(max_length=64)
    date = models.DateTimeField(default=timezone.now)
    expire = models.IntegerField(default=300)
    def __unicode__(self):
        return '%s: %s' %(self.host.host.ip_addr,self.token)