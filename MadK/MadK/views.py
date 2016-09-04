from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return render(request, 'index.html')
