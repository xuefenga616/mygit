from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

def home(request):
    return render(request,'home.html')

def son1(request):
    return render(request,'son1.html')

def login(request):
    print request.method
    if request.method == 'POST':
        input_email = request.POST.get('email')
        input_pwd = request.POST.get('pwd')
        if input_email == 'xuefeng_11@qq.com' and input_pwd == '123456':
            return redirect("/son1/")
        else:
            return render(request,'login.html',{'status':"wrong with username or password!"})
    return render(request,'login.html')