#coding:utf-8
from django.db import models

# Create your models here.
from web.models import UserProfile

class ChatGroup(models.Model):  #QQ群
    name = models.CharField(max_length=64,unique=True)
    members = models.ManyToManyField(UserProfile,blank=True)    #m2m可以不要null=True
    admins = models.ManyToManyField(UserProfile,related_name='group_admins')     #管理员
    description = models.CharField(max_length=255,default="nothing...")
    max_member_nums = models.IntegerField(default=200)
    def __unicode__(self):
        return self.name