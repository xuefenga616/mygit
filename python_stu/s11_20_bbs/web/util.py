#coding:utf-8
__author__ = 'xuefeng'
import os

def handle_uploaded_file(request,f):
    print "--->",f.name
    base_img_upload_path = 'statics/img'
    user_path = '%s/%s' %(base_img_upload_path,request.user.userprofile.id)
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    with open('%s/%s' %(user_path,f.name),'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

    alias_path = "/static/img/%s/%s" %(request.user.userprofile.id,f.name)

    return alias_path