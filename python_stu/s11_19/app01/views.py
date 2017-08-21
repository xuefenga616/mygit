#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from forms import account as AccountForm
from forms import home as HomeForm
import json
import models
from forms import foreign as ForeignForm

# Create your views here.
def login(request):
    obj = AccountForm.LoginForm(request.POST)
    if request.method == 'POST':
        if obj.is_valid():
            all_data = obj.clean()
        else:
            errors = obj.errors     # Form表单提交
            errors_str = obj.errors.as_json()
            #print errors_str
        return render(request,'account/login.html',{'obj':obj, 'errors':errors})
    else:
        return render(request,'account/login.html',{'obj':obj})

def index(request):
    # models.UserInfo.objects.all().delete()
    # models.UserInfo.objects.create(name='alex')
    # after = models.UserInfo.objects.all()
    #
    # print after[0].ctime

    # dic = {
    #     'username': 'alex',
    #     'password': '123456',
    # }
    # models.SimpleModel.objects.create(**dic)
    ret = models.SimpleModel.objects.all().values('id','username')   #取出列的k,v
    #ret = models.SimpleModel.objects.all().values_list('id','username')   #取出列的值
    print ret

    obj = HomeForm.ImportForm()
    return render(request,'home/index.html',{'obj':obj})

def upload(request):
    if request.method == 'POST':
        inp_post = request.POST
        inp_files = request.FILES
        file_obj1 = inp_files.get('f1')
        #print file_obj1,type(file_obj1)
        #from django.core.files.uploadedfile import InMemoryUploadedFile
        f = open('upload/%s' %file_obj1.name,'wb')
        for line in file_obj1.chunks():
            f.write(line)
        f.close()
    return render(request,'home/upload.html')

def foreign(request):
    models.UserGroup_new.objects.create(caption='CE0')
    models.UserGroup_new.objects.create(caption='CT0')
    models.UserGroup_new.objects.create(caption='COO')
    # models.UserGroup_new.objects.filter(id__in=[1,2,3]).delete()

    return HttpResponse('OK')

def create_user(request):
    obj = ForeignForm.UserForm(request.POST)
    if request.method == 'POST':
        if obj.is_valid():
            all_data = obj.clean()
            print all_data

            # models.User_new.objects.create(
            #     username=all_data['username'],
            #     user_group_id = all_data['user_group']       # 外键在数据库存的key是user_group_id
            # )
            models.User_new.objects.create(**all_data)
            print models.User_new.objects.all().count()

        else:
            pass
    elif request.method == 'GET':
        # val =request.GET.get('username')
        # user_list = models.User_new.objects.filter(username=val)
        val = request.GET.get('usergroup')
        user_list = models.User_new.objects.filter(user_group__caption=val)

    # user_list = models.User_new.objects.all()
    return render(request,'foreign/create_user.html',{'obj':obj,'user_list':user_list})
