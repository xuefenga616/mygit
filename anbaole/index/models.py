#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model): #用户认证
    user = models.OneToOneField(User)   #关联User类，相当于继承
    name = models.CharField(max_length=64,unique=True)

    def __unicode__(self):
        return self.name