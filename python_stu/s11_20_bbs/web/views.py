#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from forms import ArticleForm
import util

# Create your views here.
def index(request):
    articles = models.Article.objects.all()
    return render(request,'index.html',{'articles':articles})

def category(request,category_id):
    articles = models.Article.objects.filter(category_id=category_id)
    return render(request,'index.html',{'articles':articles})

def article_detail(request,article_id):
    try:
        article_obj = models.Article.objects.get(id=article_id)
        return render(request,'article.html',{'article_obj':article_obj})
    except ObjectDoesNotExist as e:
        return render(request,'404.html',{'err_msg':u'文章不存在'})

def acc_login(request):
    if request.method == 'POST':
        #print request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)     #登录
            return HttpResponseRedirect('/web/')
        else:
            err_msg = "Wrong username or password!"
            return render(request,'login.html',{'err_msg':err_msg})
    return render(request,'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/web/')

def new_article(request):
    if request.method == 'POST':
        #print request.POST
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            form_data = form.clean()
            form_data['author_id'] = request.user.userprofile.id

            new_img_path = util.handle_uploaded_file(request,request.FILES['head_img'])
            form_data['head_img'] = new_img_path

            new_article_obj = models.Article(**form_data)
            new_article_obj.save()
            return render(request,'new_article.html',{
                'new_article_obj':new_article_obj
            })
        else:
            print "err:",form.errors()
    category_list = models.Category.objects.all()
    return render(request,'new_article.html',{'categroy_list':category_list})
