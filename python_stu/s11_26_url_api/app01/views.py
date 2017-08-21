from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.

def acc_login(request):
    print request.POST
    ret = render(request,'login.html')
    ret.set_cookie('k1','v1')
    return ret