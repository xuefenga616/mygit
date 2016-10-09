#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ################################################################################

    Copyright (C),2016,落叶秋风
    文件名:  searchfan.py
    作者:    落叶秋风
    版本:    1.3
    创建日期:    2016/7/6
    完成日期:    2016/7/7

    描述: 实现读取番号并自动搜索下载链接并写入文件，同时做好相应的记录功能

    ################################################################################
"""
import re
import sys
import urllib2
import os

reload(sys)
sys.setdefaultencoding('utf-8')

historyOfFanhao=[]                                                              # 读取过的番号历史

# 链接搜寻函数
def query_magnet(key):
    data = []
    try:
        url = 'http://www.btmayi.me/search/%s-first-asc-1' % key
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        response = urllib2.urlopen(request)
        restr = re.compile(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''')
        html = response.read()
        href_list = re.findall(restr,html)
        for href_tup in href_list:
            for href in href_tup:
                if href.find("magnet:?") != -1:
                    data.append(href)
    except Exception, e:
        print e
    finally:
        return data

# 网页代码读取函数
def getUrl_multiTry(url):
    maxTryNum = 10
    html = ''
    for tries in range(maxTryNum):
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
            response = urllib2.urlopen(request)
            html = response.read()
            break
        except:
            if tries < (maxTryNum-1):
                continue
            else:
                print "Has tried %d times to access url %s, all failed!" % (maxTryNum, url)
                break
    return html

# 番号所搜函数
def searchfan():
    try:
        fanhao = re.compile(r'[A-Za-z]{2,4}-\d{2,5}')                                              # 番号正则表达式
        maxpage = re.compile('<span>\d{1,5}/(.*?) </span>')                                        # 最大页数正则表达式
        moviename = re.compile('<a target="_blank" href="/avzuopin/\d{6}/\d{6}.html">(.*?)</a></li>')# 小电影名称正则表达式
        actor = re.compile('<li class="f3">(.*?)</li><li class="f4">')                             # 演员正则表达式
        publishdata = re.compile('<li class="f4">(\d{4}-\d{2}-\d{2})</li>')                        # 发行日期正则表达式
        htmls = getUrl_multiTry('http://fanhao.mmdaren.com/avzuopin/')
        maxpages = re.findall(maxpage, htmls)

        if not os.path.exists("E:\\fanhao.txt"):                                                    # 创建fanhao.txt
            f = open("E:\\fanhao.txt", "w")
            f.close()
        else:                                                                                       # 存在就不处理
            pass

        for i in range(1, int(maxpages[0])+1):
            print "正在搜寻第%d个网页"% i

            if i == 1:
                url = 'http://fanhao.mmdaren.com/avzuopin/'
                print url
            else:
                url = 'http://fanhao.mmdaren.com/avzuopin/zuopin_%s.html' % i
                print url

            html = getUrl_multiTry(url)
            if html:                                                                            # 网页代码读取成功情况处理
                fanhao_list = re.findall(fanhao, html)
                moviename_list = re.findall(moviename, html)
                actor_list = re.findall(actor, html)
                publishdata_list = re.findall(publishdata, html)

                for j in range(len(fanhao_list)):
                    if fanhao_list[j]+'\n' not in historyOfFanhao:                              # 番号不在下载历史中情况处理
                        data = query_magnet(fanhao_list[j])                                     # 下载链接获取
                        if data:                                                                # 下载链接不为空情况处理
                            f = open("E:\\fanhao.txt", "a")
                            f.writelines(fanhao_list[j].ljust(12)+"\t"+moviename_list[j].ljust(40)+"\t"+actor_list[j]+"\t"+publishdata_list[j].ljust(10)+"\n")
                            print fanhao_list[j].ljust(12)+"\t"+moviename_list[j].ljust(40)+"\t"+actor_list[j]+"\t"+publishdata_list[j].ljust(10)+"\n"
                            f.writelines("下载链接:\n")
                            for k in range(len(data)):
                                f.write(data[k]+"\n")
                            f.write("\n\n")
                            historyOfFanhao.append(fanhao_list[j])
                            file = open("E:\\historyfanhao.txt", "a")                           # 番号下载历史写入
                            file.write(fanhao_list[j]+'\n')
                            file.close()
                            f.close()
                        else:                                                                   # 下载链接为空情况处理
                            f = open("E:\\fanhao.txt", "a")
                            f.writelines(fanhao_list[j].ljust(12)+"\t"+moviename_list[j].ljust(40)+"\t"+actor_list[j]+"\t"+publishdata_list[j].ljust(10)+"\n")
                            print fanhao_list[j].ljust(12)+"\t"+moviename_list[j].ljust(40)+"\t"+actor_list[j]+"\t"+publishdata_list[j].ljust(10)+"\n"
                            f.writelines("下载链接:\n")
                            f.write("暂无"+"\n\n\n")
                            file = open("E:\\historyfanhao.txt", "a")                           # 番号下载历史写入
                            file.write(fanhao_list[j]+'\n')
                            file.close()
                            f.close()
                    else:                                                                           # 番号在下载历史中情况处理
                        print "番号%s重复，跳出！！！" % fanhao_list[j]
                print "搜寻第%d个网页完毕"% i
            else:                                                                                   # 网页代码读取失败处理
                print "网页读取失败！！！"
        print "搜索成功！！！"
    except Exception, e:
        print e
    finally:
        f.close()

# 番号搜寻历史读取
def ReadFanhaoHistory():
    if not os.path.exists("E:\\historyfanhao.txt"):
        f = open("E:\\historyfanhao.txt", "w")
        f.close()
    else:
        pass

    f = open("E:\\historyfanhao.txt")
    try:
        OldSign = f.readline()
        while OldSign:
            historyOfFanhao.append(OldSign)
            OldSign = f.readline()
        print historyOfFanhao
    except Exception, err:
        print err
    finally:
        f.close()

if __name__ == "__main__":
    ReadFanhaoHistory()
    searchfan()
