#coding:utf-8
__author__ = 'Administrator'

from BrightEye import settings
import os,tempfile,zipfile
from django.http import HttpResponse
import models
from django.utils import timezone
from wsgiref.util import FileWrapper


def recent_accessed_hosts(request):
    #days_before_14 = timezone.now() + timezone.timedelta(days=-14)  #两周之前
    #recent_logins = models.AuditLog.objects.filter(date__gt=days_before_14,user_id=request.user.userprofile.id,action_type=1).order_by('date')
    pass

def handle_upload_file(request,file_obj):
    upload_dir = '%s\\%s\\%s' %(settings.BASE_DIR,settings.FileUploadDir,request.user.userprofile.id)
    print upload_dir
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)

    with open('%s\\%s' %(upload_dir,file_obj.name),'wb') as dest:
        for chunk in file_obj.chunks():
            dest.write(chunk)

    return '%s\\%s' %(upload_dir,file_obj.name)

def send_tmpfile(request,task_id,file_path):
    zip_file_name = 'taskid_%s_files' %task_id
    archive = zipfile.ZipFile(zip_file_name , 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write('%s\\%s' %(file_path,filename))
    archive.close()
    wrapper = FileWrapper(file(zip_file_name))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
    response['Content-Length'] = os.path.getsize(zip_file_name)
    #temp.seek(0)
    return response
