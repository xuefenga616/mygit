#coding:utf-8
from django.shortcuts import render

# Create your views here.
import models

class Pager(object):
    def __init__(self,current_page):
        self.current_page = int(current_page)

    @property    #方法改属性,调用时不加括号
    def start(self):
        return (self.current_page - 1) * 10

    @property
    def end(self):
        return self.current_page * 10

    def page_str(self,all_item,base_url):
        all_page,div = divmod(all_item,10)   #div代表余数
        if div > 0:     #如果不能整除，有余数
            all_page += 1

        pager_list = []
        # 默认用户看到的页码是11个
        start = self.current_page -5
        end = self.current_page + 5
        if all_page < 11:
            start = 1
            end = all_page
        elif start < 1:
            start = 1
            end = 11
        elif end > all_page:
            end = all_page
            start = end - 10
        for i in range(start,end+1):
            if i == self.current_page:  #加样式
                temp = '<a style="color:red;font-size:20px" href="%s%d">%d</a>' %(base_url,i,i)
            else:
                temp = '<a href="%s%d">%d</a>' %(base_url,i,i)
            pager_list.append(temp)
        #上一页
        if self.current_page > 1:
            pre_page = '<a href="%s%d">上一页</a>' %(base_url, self.current_page-1)
        else:
            pre_page = '<a href="javascript:void(0);">上一页</a>'   #javascript:void(0);表示什么都不做
        if self.current_page >= all_page:
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = pre = '<a href="%s%d">下一页</a>' %(base_url, self.current_page+1)
        pager_list.insert(0,pre_page)
        pager_list.append(next_page)

        return "".join(pager_list)


def user_list(request):
    # for item in range(100):
    #     temp = {'username':"name%d" %item,
    #             'age': item}
    #     models.UserList.objects.create(**temp)
    #每页显示10条数据
    #向用户获取一个页面
    # ?a=9&b=10  ->  request.GET.get('a',0)   #后端拿url里配的参数，没有取到则设置为0
    current_page = request.GET.get('page',1)   #后端拿url里配的参数，没有取到则设置为1
    # current_page = int(current_page)
    # start = current_page * 10 - 10  #0  10
    # end = current_page * 10         #10 20
    page_obj = Pager(current_page)
    result = models.UserList.objects.all()[page_obj.start: page_obj.end]
    print result.query

    all_item = models.UserList.objects.all().count()
    pager_str = page_obj.page_str(all_item,"/user_list/?page=")

    return render(request,'user_list.html',{'result':result,'pager_str':pager_str})