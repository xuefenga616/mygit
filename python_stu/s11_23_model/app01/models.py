#coding:utf-8
from django.db import models

# Create your models here.

class UserType(models.Model):
    caption = models.CharField(max_length=32)

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    age = models.SmallIntegerField()
    user_type = models.ForeignKey('UserType')

##################################################

class MyUser(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    def __unicode__(self):
        return self.username

class News(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=128)
    def __unicode__(self):
        return self.title

class Favor(models.Model):
    user = models.ForeignKey("MyUser")
    news = models.ForeignKey("News")
    def __unicode__(self):
        return "%s -> %s" %(self.user.username,self.news.title)

##################################################

class Host(models.Model):
    hostname = models.CharField(max_length=32)
    port = models.IntegerField()
    def __unicode__(self):
        return self.hostname

class HostAdmin(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    host = models.ManyToManyField("Host")
    def __unicode__(self):
        return self.username

class HostAdmin2(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    host = models.ManyToManyField("Host",through="HostRelation")
    def __unicode__(self):
        return self.username

class HostRelation(models.Model):
    c1 = models.ForeignKey("Host")
    c2 = models.ForeignKey("HostAdmin2")

