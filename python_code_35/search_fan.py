#coding:utf-8
__author__ = 'Administrator'
import requests
from bs4 import BeautifulSoup
import re

def getHtml(urlJoin):  #链接搜寻函数
    html = requests.get(urlJoin).text.encode('utf-8')
    return html

queryUrl = "http://www.btany.com/search/%s-first-asc-1"

def query_magnet(key):
    urlJoin = queryUrl %key
    queryPage = getHtml(urlJoin)
    soupQuery = BeautifulSoup(queryPage,"html.parser")
    for content in soupQuery.find_all('div',class_='search-item'):
        query_title = content.find('div',class_='item-list').get_text().strip()
        thunder_links = content.find('div',class_='item-bar').find_all('a',class_='download')
        print(query_title)
        for thunder_link in thunder_links:
            link = thunder_link.get('href')
            print(link)
        print('\r\n')



query_magnet('dd')

#http://club.huawei.com/search.php?mod=forum&searchid=17390507&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=dd


