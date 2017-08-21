#coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

# Create your views here.
import models,json,Queue,time

GLOBAL_MQ = {}  #用来存放消息

def web_chat(request):
    return render(request,'web_chat/chat.html')

def contacts(request):
    contact_dic = {}

    contacts = request.user.userprofile.friends.select_related().values('id','name')    #values()是直接取值
    contact_dic['contact_list'] = list(contacts)    #强制转成list
    groups = request.user.userprofile.chatgroup_set.select_related().values('id','name','max_member_nums')    #反查
    contact_dic['group_list'] = list(groups)
    #print contact_dic

    return HttpResponse(json.dumps(contact_dic))

def new_msg(request):
    if request.method == "POST":
        print request.POST.get('data')
        data = json.loads(request.POST.get('data'))
        send_to = data['to']
        if send_to not in GLOBAL_MQ:
            GLOBAL_MQ[send_to] = Queue.Queue()
        data['timestamp'] = time.time()
        GLOBAL_MQ[send_to].put(data)    #放到消息队列中

        return HttpResponse(GLOBAL_MQ[send_to].qsize())
    else:
        request_user = str(request.user.userprofile.id)     #因为id取出来是int类型
        msg_list = []
        if request_user in GLOBAL_MQ:    #存放消息的字典中有自己，则取出属于自己的消息
            stored_msg_nums = GLOBAL_MQ[request_user].qsize()
            if stored_msg_nums == 0:
                ##没有新消息,开始长轮循
                print "\033[41;1m No new msg, wait for 3 secs...\033[0m"
                try:
                    msg_list.append(GLOBAL_MQ[request_user].get(timeout=3))  #get()是阻塞状态,超时会抛异常
                except Exception as e:
                    print e
                    print "\033[41;1m Time out or new msgs...\033[0m"
            for i in range(stored_msg_nums):    #有几条则取几次
                msg_list.append(GLOBAL_MQ[request_user].get())
        else:
            #create a new queue for this user
            GLOBAL_MQ[request_user] = Queue.Queue()
        return HttpResponse(json.dumps(msg_list))
