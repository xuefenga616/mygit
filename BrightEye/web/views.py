#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import models
import json,datetime
from BrightEye import settings
from django.core.exceptions import ObjectDoesNotExist
import host_mgr
import utils
import os

@login_required
def dashboard(request):
    return render(request,'index.html')

def acc_login(request):
    login_err = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                auth.login(request,user)
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return render(request,'login.html',{'login_err':u'BrightEye账户还未设定，请先登录后台管理界面创建BrightEye账户!'})
        else:
            return render(request,'login.html',{'login_err':'Wrong username or password!'})
    else:
        return render(request,'login.html')

@login_required
def acc_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def hosts(request):
    selected_g_id = request.GET.get('selected_group')
    if selected_g_id.isdigit():
        selected_g_id = int(selected_g_id)

    return render(request,'hosts.html',{'login_user':request.user,
                                        'selected_g_id':selected_g_id,
                                        'active_node':"/hosts/?selected_group=-1",
                                        'webssh':settings.SHELLINABOX})

@login_required
def hosts_multi(request):
    return render(request,'hosts_multi.html',{'login_user':request.user,
                                              'active_node':'/hosts/multi'})
@login_required
def multitask_cmd(request):
    print request.POST
    multi_task = host_mgr.MultiTask('run_cmd',request)
    task_id = multi_task.run()
    if task_id:
        return HttpResponse(task_id)
    else:
        return HttpResponse("TaskCreatingError")

@login_required
def multitask_res(request):
    multi_task = host_mgr.MultiTask('get_task_result',request)
    task_result = multi_task.run()
    return HttpResponse(task_result)

@login_required
def hosts_multi_filetrans(request):
    return render(request,'hosts_multi_files.html',{'login_user':request.user,
                                                    'active_node':'/hosts/multi_filetrans'})

@login_required
@csrf_exempt
def multitask_file_upload(request):
    filename = request.FILES['filename']
    print '-->',request.POST
    file_path = utils.handle_upload_file(request,filename)

    return HttpResponse(json.dumps({'uploaded_file_path':file_path,
                                    'text':'success'}))

@login_required
def file_download(request,task_id): #下载文件到我的电脑
    file_path = "%s\\%s\\%s" %(settings.BASE_DIR,settings.FileUploadDir,request.user.userprofile.id)

    return utils.send_tmpfile(request,task_id,file_path)

@login_required
def multitask_file(request):
    print 'multitask_file',request.POST
    multi_task = host_mgr.MultiTask(request.POST.get('task_type'),request)
    task_id = multi_task.run()
    return HttpResponse(task_id)

@login_required
def hosts_crontab(request):
    return render(request,'crontab.html',{'active_node':'/hosts/crontab'})

@login_required
def multitask_bigtask(request):
    print 'multitask_bigtask',request.POST
    multi_task = host_mgr.MultiTask(request.POST.get('task_type'),request)
    task_id = multi_task.run()
    return HttpResponse(task_id)

@login_required
def bigtask_log(request,task_id):
    local_path = "%s\\%s\\%s" %(settings.BASE_DIR,settings.FileUploadDir,request.user.userprofile.id)
    bigtask_obj = models.TaskLog.objects.get(id=int(task_id))
    conf_dic = bigtask_obj.cmd
    conf_dic = json.loads(conf_dic)
    #print conf_dic
    multi_task = host_mgr.Bigtask_exec(task_type='bigtask_exec',local_path=local_path,**conf_dic)
    cmd_result = multi_task.run()

    return render(request,'bigtask_log.html',{'task_id':task_id,
                                              'log':cmd_result})