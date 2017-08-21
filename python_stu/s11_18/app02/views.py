#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.
from django import forms
import re
from django.core.exceptions import ValidationError

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError(u'手机号码格式错误')

class UserInfo(forms.Form): #django的表单验证
    user_type_choices = (
        (0, u'普通用户'),
        (1, u'高级用户'),
    )
    user_type = forms.IntegerField(widget=forms.widgets.Select(choices=user_type_choices,
                                    attrs={'class':'form-control'}))

    email = forms.EmailField(error_messages={'required':u'邮箱不能为空'})
    host = forms.CharField(error_messages={'required':u'主机不能为空'})
    port = forms.CharField(error_messages={'required':u'端口不能为空'})
    mobile = forms.CharField(error_messages={'required':u'手机不能为空'},
                             validators=[mobile_validate,],     #校验
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':u'mobile phone'}))
    memo = forms.CharField(required=False,
                           widget=forms.Textarea(attrs={'class':'form-control','placeholder':u'memo'}))  #required=False,表示可以为空


def user_list(request):
    obj = UserInfo()
    if request.method == 'POST':
        user_input_obj = UserInfo(request.POST)
        #开始验证:
        print user_input_obj.is_valid()     #合法返回True，不合法返回False
        if user_input_obj.is_valid():
            data = user_input_obj.clean()
            print data
        else:
            error_msg = user_input_obj.errors
            #print error_msg
            return render(request,'user_list.html',{'obj':user_input_obj,'error_msg':error_msg})
    return render(request,'user_list.html',{'obj':obj})

def user_list2(request):
    return render(request,'user_list2.html')

def ajax_data(request):
    print request.POST
    return HttpResponse('OK')