#coding:utf-8
__author__ = 'Administrator'
import requests,re,exceptions

class spider():
    def __init__(self):
        print "spider starting......"
    def getSource(self,url):
        html = requests.get(url).text
        return html
    def changePage(self,url,num_total):
        changePage = []
        for each in range(1,num_total+1,50):
            urlNow = re.sub('pn=(\d)','pn=%s'%each,url,re.S) #使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配
            changePage.append(urlNow)
        return changePage
    def getMyideaInfo(self,source):
        li = re.findall('<li class=" j_thread_list clearfix"(.*?)</li>',source,re.S)
        return li
    def getinfo(self,classinfo):
        info = {}
        info['最后回复日期'] = re.findall('title="最后回复时间">(.*?)</span>',classinfo,re.S)
        info['回复人数'] = re.findall('title="回复">(.*?)</span>',classinfo,re.S)
        info['主题'] = re.findall('target="_blank" class="j_th_tit ">(.*?)</a>',classinfo,re.S)
        info['主题作者'] = re.findall('title="主题作者: (.*?)"',classinfo,re.S)
        info['内容'] = re.findall('threadlist_abs threadlist_abs_onlyline ">(.*?)</div>',classinfo,re.S)
        return info
    def saveinfo(self,info):
        with open('D:\spider\infoTieba.txt','a') as f:
            for each in info:
                try:
                    f.writelines('回复人数：' + ''.join(each['回复人数']) + '\n')
                    f.writelines('最后回复日期：' + ''.join(each['最后回复日期']) + '\n')
                    f.writelines('主题：' + ''.join(each['主题']).encode('utf-8') + '\n')
                    f.writelines('主题作者：' + ''.join(each['主题作者']).encode('utf-8') + '\n')
                    f.writelines('内容：' + ''.join(each['内容']).encode('utf-8') + '\n')
                except Exception,e:
                    print e


if __name__ == '__main__':
    classInfo = []
    url = "http://tieba.baidu.com/f?ie=utf-8&kw=%E6%B9%96%E5%8C%97%E5%A4%A7%E5%AD%A6&fr=search"
    mySpider = spider()
    netPage = mySpider.changePage(url,200)
    for each in netPage:
        print "正在处理： ",each
        html = mySpider.getSource(each)
        myidea = mySpider.getMyideaInfo(html)
        for i in myidea:
            info = mySpider.getinfo(i)
            classInfo.append(info)
    mySpider.saveinfo(classInfo)
