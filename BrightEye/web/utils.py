#coding:utf-8
__author__ = 'Administrator'

from BrightEye import settings
import os
from django.http import HttpResponse
import models
from django.utils import timezone


def recent_accessed_hosts(request):
    #days_before_14 = timezone.now() + timezone.timedelta(days=-14)  #两周之前
    #recent_logins = models.AuditLog.objects.filter(date__gt=days_before_14,user_id=request.user.userprofile.id,action_type=1).order_by('date')
    pass