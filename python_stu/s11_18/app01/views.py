#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.
import time
from django.views.decorators.cache import cache_page    #缓存装饰器

@cache_page(60 * 1)    # 1分钟过期
def cache_page(request):
    current = str(time.time())
    return HttpResponse(current)

def index(request):
    print "get index!"
    #raise Exception("bbbbbbbbbbbbb")
    return HttpResponse('OK')

# def user_list(request,nid,page):
#     print nid,page
#     return HttpResponse(nid+page)

def user_list(request,v2,v1):
    print v1,v2
    return HttpResponse(v1+v2)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        if username == 'alex' and pwd == '123456':
            request.session['IS_LOGIN'] = True
            request.session['USERNAME'] = username
            return HttpResponseRedirect("/app01/home/")
        else:
            return render(request,'login.html')
    return render(request,'login.html')

def logout(request):
    del request.session['IS_LOGIN']
    return HttpResponseRedirect('/app01/home/')

def home(request):
    is_login = request.session.get('IS_LOGIN')
    if is_login:
        username = request.session.get('USERNAME')
        return render(request,'home.html',{'username':username})
    else:
        return HttpResponseRedirect('/app01/login/')

