#coding:utf-8
__author__ = 'xuefeng'
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

class mmm(object):
    def process_request(self,request):
        print "mmm.process_request"

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print "mmm.process_view"

    def process_response(self, request, response):
        print "mmm.process_response"
        return response

    def process_exception(self,request,exception):
        print "mmm.exception:",exception
        return HttpResponse("mmm.process_exception")


class nnn(object):
    def process_request(self,request):
        print "nnn.process_request"

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print "nnn.process_view"

    def process_response(self, request, response):
        print "nnn.process_response"
        return response

    def process_exception(self,request,exception):
        print "nnn.exception:",exception
        #return HttpResponse("nnn.process_exception")