from django.shortcuts import render,HttpResponse
import core
import json
import models

# Create your views here.

def asset_report(request):
    print request.GET
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid():
            ass_handler.data_inject()
        return HttpResponse(json.dumps(ass_handler.response))
    return HttpResponse('--test--')

def asset_with_no_asset_id(request):
    pass

def new_assets_approval(request):
    pass

def asset_report_test(request):
    pass

def acquire_asset_id_test(request):
    pass

def asset_list(request):
    pass

def get_asset_list(request):
    pass

def asset_event_logs(request):
    pass

def asset_detail(request):
    pass