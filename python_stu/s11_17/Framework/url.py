#coding:utf-8
__author__ = 'xuefeng'
from Controllers import home

urlpatterns = (
    ('/index/',home.index),
    ('/login/',home.login),
)
