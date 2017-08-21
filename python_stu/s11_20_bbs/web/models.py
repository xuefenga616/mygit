#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(u'文章标题',max_length=255,unique=True)
    category = models.ForeignKey("Category",verbose_name=u'版块')
    head_img = models.ImageField(upload_to="uploads")
    summary = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey("UserProfile")
    publish_date = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=False)      #是否隐藏
    priority = models.IntegerField(u'优先级',default=1000)
    def __unicode__(self):
        return "<%s, author:%s>" %(self.title,self.author)

class Comment(models.Model):
    article = models.ForeignKey("Article")
    user = models.ForeignKey("UserProfile")
    comment = models.TextField(max_length=1000)
    parent_comment = models.ForeignKey("Comment",related_name='pComment',null=True,blank=True)   #父评论，自关联
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "<%s, user:%s>" %(self.comment,self.user)

class ThumbUp(models.Model):    #点赞
    article = models.ForeignKey("Article")
    user = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "<user:%s>" %self.user

class Category(models.Model):   #版块表
    name = models.CharField(max_length=64,unique=True)
    admin = models.ManyToManyField("UserProfile")        #版块管理员
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    groups = models.ManyToManyField("UserGroup")
    ####### web chat ##########
    friends = models.ManyToManyField("UserProfile",related_name="my_friends")
    def __unicode__(self):
        return self.name

class UserGroup(models.Model):
    name = models.CharField(max_length=64,unique=True)
    def __unicode__(self):
        return self.name


