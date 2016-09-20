from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import models
import json

# Create your views here.
def index(request):
    return render(request,'index.html')

def cart(request):
    return render(request,'index_web/cart.html')

def acc_login(request):
    login_err = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            login_err = "Wrong username or password!"
    return render(request,'login.html',{'login_err':login_err})

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    return render(request,'register.html')