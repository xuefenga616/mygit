#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.
import models
from django.db.models import F,Q

def user_type(request):
    # dic = {'caption':'COO'}
    # models.UserType.objects.create(**dic)
    # print models.UserType.objects.all().count()
    return HttpResponse("OK")

def user_info(request):
    # dic = {'username':'alex','age':25,'user_type_id':1}
    # dic = {'username':'jack','age':25,'user_type':models.UserType.objects.get(id=2)}
    # models.UserInfo.objects.create(**dic)
    # result = models.UserInfo.objects.all()
    # for item in result:
    #     print item.username,item.age,item.user_type.caption

    #正向查找
    result = models.UserInfo.objects.filter(user_type__caption='CEO')
    for item in result:
        print item.username,item.age,item.user_type.caption
    #反向查找
    result = models.UserType.objects.get(caption='CTO').userinfo_set.all()
    for item in result:
        print item.username,item.age,item.user_type.caption

    user_type_obj = models.UserType.objects.get(userinfo__username='alex')
    result = user_type_obj.userinfo_set.all()
    for item in result:
        print item.username,item.age,item.user_type.caption

    # news_list = models.News.objects.all()
    news_list = models.News.objects.filter(favor__user__username='alex')
    for news in news_list:
        print "="*20
        print news.title
        print news.content
        print news.favor_set.all().count()

    # dic01 = {'hostname':'lvs-01','port':22}
    # dic02 = {'hostname':'lvs-02','port':22}
    # dic03 = {'hostname':'web-01','port':80}
    # dic04 = {'hostname':'web-02','port':80}
    # models.Host.objects.create(**dic01)
    # models.Host.objects.create(**dic02)
    # models.Host.objects.create(**dic03)
    # models.Host.objects.create(**dic04)
    # print models.Host.objects.all().count()
    # models.HostAdmin.objects.create(username='alex',email="1@live.com")
    # models.HostAdmin.objects.create(username='jack',email="2@live.com")
    # models.HostAdmin.objects.create(username='joe',email="3@live.com")
    # print models.HostAdmin.objects.all().count()
    # 添加数据
    # 正向添加
    # admin_obj = models.HostAdmin.objects.get(username='alex')
    # host_list = models.Host.objects.filter(id__lt=3)    #id < 3
    # admin_obj.host.add(*host_list)
    # 反向添加
    # host_obj = models.Host.objects.get(id=2)
    # admin_list = models.HostAdmin.objects.filter(id__gt=1)
    # host_obj.hostadmin_set.add(*admin_list)

    # models.HostRelation.objects.create(
    #     c1_id = 1,
    #     c2_id = 1
    # )
    # 正向查询
    # models.HostAdmin.objects.get(id=1).host.all()
    # 反向查询
    # models.Host.objects.get(id=1).hostadmin_set.all()
    relation_list = models.HostRelation.objects.filter(c2__username='alex')
    for item in relation_list:
        print item.c1.hostname
        print item.c2.username

    ret = models.UserInfo.objects.all().select_related()
    print ret.query

    return HttpResponse("OK")
