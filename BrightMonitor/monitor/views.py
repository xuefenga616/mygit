#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import serializer
import models
import json,time
from backends import data_optimization
import graphs

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def index(request):
    return render(request,"index.html")

def hosts(request):
    host_list = models.Host.objects.all()
    return render(request,'hosts.html',{'host_list':host_list})

def client_configs(request,client_id):
    print "--->",client_id
    config_obj = serializer.ClientHandler(client_id)
    config = config_obj.fetch_configs()

    return HttpResponse(json.dumps(config))

@csrf_exempt
def service_data_report_bak(request):
    if request.method == 'POST':
        print "---->",request.POST
        try:
            print "host=%s, service=%s" %(request.POST.get('client_id'),request.POST.get('service_name'))
            client_id = request.POST.get('client_id')
            service_name = request.POST.get('service_name')

            data = json.loads(request.POST['data'])
            print data
            #data_saving_obj = data_optimization.DataStore(client_id,service_name,data)

        except IndexError,e:
            print "----->err:",e

    return HttpResponse(json.dumps("---report success---"))



def hosts_status(request):
    hosts_data_serializer = serializer.StatusSerializer(request)
    hosts_data = hosts_data_serializer.by_hosts()
    return HttpResponse(json.dumps(hosts_data))

def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request,'host_detail.html',{'host_obj':host_obj})

def trigger_list(request):
    trigger_handle_obj = serializer.TriggersView(request)
    trigger_data = trigger_handle_obj.fetch_related_filters()
    return render(request,'trigger_list.html',{'trigger_list':trigger_data})

def graphs_gerator(request):
    graphs_gerator = graphs.GraphGenerator(request)
    graphs_data = graphs_gerator.get_host_graph()

    return HttpResponse(json.dumps(graphs_data))

