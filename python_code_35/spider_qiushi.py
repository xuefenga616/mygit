#coding:utf-8
__author__ = 'Administrator'
import requests
from bs4 import BeautifulSoup

def getContentOrComment(urlJoin):  #链接搜寻函数
    html = requests.get(urlJoin).text
    return html

articleUrl = "http://www.qiushibaike.com/textnew/page/%d"   #文章第几页
commentUrl = "http://www.qiushibaike.com/article/%s"        #评论地址

page = 0
tmp_list = []
while int(page)<1:
    page += 1
    urlJoin = articleUrl %page
    print(urlJoin)
    tmp_list.append(urlJoin)
    articlePage = getContentOrComment(urlJoin)
    soupArticle = BeautifulSoup(articlePage,'html.parser')

    articleFloor = 1
    for string in soupArticle.find_all(attrs="article block untagged mb15"):
        commentId = str(string.get('id')).strip()[11:]  #取评论id号
        a_str = str(articleFloor) + ". " + string.find(attrs="content").get_text().strip()
        print(a_str)
        tmp_list.append(a_str)
        articleFloor += 1
        commentPage = getContentOrComment(commentUrl %commentId)
        soupCommnet = BeautifulSoup(commentPage,'html.parser')
        commentFloor = 1
        for comment in soupCommnet.find_all(attrs="body"):
            c_str = "    " + str(commentFloor) + "楼回复：" + comment.get_text().strip()
            print(c_str)
            tmp_list.append(c_str)
            commentFloor += 1
with open('d:\spider\qiushi.txt','a+') as f:
    f.write('\n'.join(tmp_list))
