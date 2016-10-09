# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import re
import HTMLParser
import cgi
import sys
import os

#处理页面标签类
class htmltool:
    #去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')

    #html 转换成txt
    #譬如 '&lt;abc&gt;' --> '<abc>'
    def html2txt(self,html):
        html_parser = HTMLParser.HTMLParser()
        txt = html_parser.unescape(html)
        return txt.strip()

    #html 转换成txt
    #譬如 '<abc>' --> '&lt;abc&gt;'
    def txt2html(self,txt):
        html = cgi.escape(txt)
        return html.strip()

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x.strip()

    #获取脚本文件的当前路径，返回utf-8格式
    def getPyFileDir(self):
        #获取脚本路径
        path = sys.path[0]
        #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path.decode('utf-8')
        elif os.path.isfile(path):
            return os.path.dirname(path).decode('utf-8')

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        pathDir = self.getPyFileDir()
        #print path
        #print pathDir
        #unicode格式
        path = u'%s\\%s' %(pathDir,path)
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            #print u'新建[%s]的文件夹\n' %(path)
            # 创建目录操作函数
            os.makedirs(path)
        #else:
           # 如果目录存在则不创建，并提示目录已存在
           #print u'文件夹[%s]已存在\n'  %(path)
        os.chdir(path)
        return  path
