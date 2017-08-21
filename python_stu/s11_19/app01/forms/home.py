#coding:utf-8
__author__ = 'xuefeng'
from django import forms
import json
from app01 import models

class ImportForm(forms.Form):
    admin = forms.IntegerField(
        widget=forms.Select(),
    )

    host_type_list = (
        (0, u'物理机'),
        (1, u'虚拟机'),
    )
    host_type = forms.IntegerField(
        widget=forms.Select(choices=host_type_list),
    )
    hostname = forms.CharField()

    def __init__(self,*args,**kwargs):
        super(ImportForm,self).__init__(*args,**kwargs)

        # with open('db_admin','r') as f:
        #     data = f.read()
        # data_tuple = json.loads(data)
        #
        # self.fields['admin'].widget.choices = data_tuple
        self.fields['admin'].widget.choices = models.SimpleModel.objects.all().values_list('id','username')