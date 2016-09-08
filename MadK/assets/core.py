#coding:utf-8
__author__ = 'Administrator'
import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import json

class Asset(object):
    def __init__(self,request):
        self.request = request
        self.mandatory_fields = ['sn', 'asset_id', 'asset_type']    #必须要有这三个值
        self.field_sets = {
            'asset': ['manufactory'],
            'server': ['model','cpu_count','cpu_core_count','cpu_model','raid_type','os_type','os_distribution','os_release'],
            'networkdevice': []
        }
        self.response = {
            'error': [],
            'info': [],
            'warning': [],
        }
    def response_msg(self,msg_type,key,msg):
        if self.response.has_key(msg_type):
            self.response[msg_type].append({key:msg})
        else:
            raise ValueError
    def mandatory_check(self,data,only_check_sn=False):
        for field in self.mandatory_fields:
            if not data.has_key(field): #没那三个值
                self.response_msg('error','MandatoryCheckFailed',"The field [%s] is mandatory and not provided in your reporting data" %field)
            else:
                if self.response['error']:  #出错
                    return False
            ###

