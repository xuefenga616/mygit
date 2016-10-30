#coding:utf-8
from django.shortcuts import render,HttpResponseRedirect,HttpResponse

# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import models,task
import json
import utils

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def hosts_index(request):
    return render(request,'hosts/dashboard.html')

@login_required
def assets_index(request):
    return render(request,'assets/dashboard.html')

@login_required
def monitor_index(request):
    return render(request,'monitor/dashboard.html')

def acc_login(request):
    login_err = ''
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            login_err = "Wrong username or password!"

    return render(request,"login.html",{'login_err':login_err})

@login_required
def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def host_mgr(request):
    selected_gid = request.GET.get('selected_gid')
    if selected_gid:
        host_list = models.BindHostToUser.objects.filter(host_groups__id=selected_gid)
    else:   #没选，即刚打开页面时，返回未分组的
        host_list = request.user.bind_hosts.select_related()
    return render(request,'hosts/host_mgr.html',{'host_list':host_list})

@login_required
def multi_cmd(request):
    return render(request,'hosts/multi_cmd.html')

@login_required
def submit_task(request):
    print request.POST
    #print request.POST.get('task_type')
    #print request.POST.get('cmd')
    #print request.POST.getlist('selected_hosts[]')

    task_obj = task.Task(request)
    res = task_obj.handle()

    return HttpResponse(json.dumps(res))

@login_required
def get_task_result(request):
    task_obj = task.Task(request)
    res = task_obj.get_task_result()
    return HttpResponse(json.dumps(res,default=utils.json_date_handler))    #dumps时可执行相关函数

@login_required
def multi_file_transfer(request):
    return render(request,'hosts/multi_file_transfer.html')

@csrf_exempt    #免除csrf验证
@login_required
def file_upload(request):
    filename = request.FILES['filename']
    print '--> ',request.POST
    file_path = utils.handle_upload_file(request,filename)  #上传文件路径及文件名

    return HttpResponse(json.dumps({'uploaded_file_path':file_path}))
