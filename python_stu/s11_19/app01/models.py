#coding:utf-8
from django.db import models

# Create your models here.
"""
类 -》数据库表
对象 -》一行数据
对象.id, 对象.value -》每行里面的数据
"""

class UserInfo(models.Model):
    user_type_list = (
        (0, 'f'),
        (0, 'm'),
    )
    user_type = models.IntegerField(choices=user_type_list,default=1)
    name = models.CharField(max_length=32,primary_key=True,unique=True,verbose_name=u'姓名')
    ctime = models.DateTimeField(auto_now=True)
    uptime = models.DateTimeField(auto_now_add=True)    #每次更新表数据时更新
    email = models.EmailField(max_length=32,null=True)
    email2 = models.EmailField(max_length=32,default="123@qq.com")
    ip = models.GenericIPAddressField(null=True)
    img = models.ImageField(null=True,upload_to="upload")

    def __unicode__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=16)

class Somthing(models.Model):
    c1 = models.CharField(max_length=10)
    c2 = models.CharField(max_length=10)
    c3 = models.CharField(max_length=10)
    c4 = models.CharField(max_length=10)
    color = models.ForeignKey('Color')

class Business(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)

class Host(models.Model):
    hostname = models.CharField(max_length=32)
    business = models.ForeignKey('Business',to_field='nid')

class UserGroup(models.Model):
    name = models.CharField(max_length=16)

class User(models.Model):
    name = models.CharField(max_length=16)
    email = models.CharField(max_length=16)
    mobile = models.CharField(max_length=16)
    user_user_group = models.ManyToManyField('UserGroup')

class AAdmin(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    user_info = models.OneToOneField('user')

class SimpleModel(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


class UserGroup_new(models.Model):

    caption = models.CharField(max_length=64)

    def __unicode__(self):
        return self.caption


class User_new(models.Model):
    username = models.CharField(max_length=64,unique=True)
    user_group = models.ForeignKey('UserGroup_new')

    def __unicode__(self):
        return self.hostname


