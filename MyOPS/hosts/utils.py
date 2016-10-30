#coding:utf-8
__author__ = 'Administrator'
import os,random
from MyOPS import settings

def json_date_handler(obj):     #把时间转化为时间戳，因为JSON不能dumps时间类型
    if hasattr(obj,'isoformat'):
        return obj.strftime("%Y-%m-%d %H:%M:%S")

def handle_upload_file(request,file_obj):
    random_dir = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',10))
    upload_dir = '%s/%s' %(settings.FileUploadDir,request.user.id)
    upload_dir2 = '%s/%s' %(upload_dir,random_dir)
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
    if not os.path.isdir(upload_dir2):
        os.mkdir(upload_dir2)

    with open('%s/%s' %(upload_dir2,file_obj.name), 'wb') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return "%s\\%s" %(random_dir,file_obj.name)      #返回文件名