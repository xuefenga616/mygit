#coding:utf-8
__author__ = 'xuefeng'
from django import forms
import json
from app01 import models

class UserForm(forms.Form):
    username = forms.CharField()
    user_group_id = forms.IntegerField(
        widget=forms.Select()
    )

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)

        self.fields['user_group_id'].widget.choices = models.UserGroup_new.objects.all().values_list('id','caption')