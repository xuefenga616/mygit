#coding:utf-8
from django.db import models

# Create your models here.

class UserList(models.Model):
    username = models.CharField(max_length=32)
    age = models.IntegerField()
