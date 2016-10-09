#coding:gbk

import urllib
import urllib2
import cookielib
import time,datetime
from PIL import Image
from lxml import etree
from ordereddict import OrderedDict
import re
import json
import htmltool
import os
import threading
import gzip
import StringIO
import requests

class HuaWei:
    #华为云服务登录
    '''
    访问http://www.hicloud.com 执行多步跳转
    1、先直接在页面中refresh跳转到http://www.hicloud.com/others/login.action
    2、再直接redirect到https://hwid1.vmall.com/casserver/logout?service=https://www.hicloud.com:443/logout
    3、再redirect到https://hwid1.vmall.com/casserver/remoteLogin?service=https://www.hicloud.com:443/others/login.action&loginChannel=1000002&reqClientType=1&loginUrl=https://hwid1.vmall.com/oauth2/account/login?reqClientType=1&lang=zh-cn&adUrl=https://www.hicloud.com:443/others/show_advert.action
    4、再redirect到https://hwid1.vmall.com/oauth2/account/login?reqClientType=1&validated=true&service=https://www.hicloud.com:443/others/login.action&loginChannel=1000002&reqClientType=1&adUrl=https://www.hicloud.com:443/others/show_advert.action&lang=zh-cn
    这个链接会刷新出来登录界面，本程序直接使用链接4进行登陆。
    5、在链接4中包含一个刷新验证码的request: https://hwid1.vmall.com/casserver/randomcode?randomCodeType=emui4_login&_t=1462786575782
    6、接下来调用https://hwid1.vmall.com/casserver/remoteLogin进行post提交
    7、登录成功后会再次执行3次redirect，分别是:
    https://www.hicloud.com:443/others/login.action?lang=zh-cn&ticket=1ST-157502-OVRaMo6aV9BcM9Sh2Dpe-cas
    https://www.hicloud.com:443/others/login.action?lang=zh-cn
    https://www.hicloud.com:443/home
    若是登录失败，会redirect到链接4，因此本文直接使用链接4进行登录。
    https://hwid1.vmall.com/oauth2/account/login?validated=true&errorMessage=random_code_error|user_pwd_continue_error&service=https%3A%2F%2Fwww.hicloud.com%3A443%2Fothers%2Flogin.action%3Flang%3Dzh-cn&loginChannel=1000002&reqClientType=1&adUrl=https%3A%2F%2Fwww.hicloud.com%3A443%2Fothers%2Fshow_advert.action%3Flang%3Dzh-cn&lang=zh-cn&viewT
    '''

    def __init__(self):
        self.username='13544270030' #用户名
        self.passwd='Xf19850917' #用户密码
        self.authcode='' #验证码
        self.baseUrl='https://hwid1.vmall.com'
        self.loginUrl=self.baseUrl+'/oauth2/account/login?reqClientType=1&validated=true&service=https://www.hicloud.com:443/others/login.action&loginChannel=1000002&reqClientType=1&adUrl=https://www.hicloud.com:443/others/show_advert.action&lang=zh-cn'
        #self.loginUrl='https://www.hicloud.com'
        self.randomUrl=self.baseUrl+'/casserver/randomcode'
        self.checkpwdUrl=self.baseUrl+'/casserver/remoteLogin'
        self.successUrl='https://www.hicloud.com:443/album'
        self.getalbumsUrl= 'https://www.hicloud.com/album/getCloudAlbums.action'
        self.getalbumfileUrl = 'https://www.hicloud.com/album/getCloudFiles.action'
        self.loginHeaders = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Connection' : 'keep-alive'
        }
        self.CSRFToken=''
        self.OnceMaxFile=100 #单次最大获取文件数量
        self.FileList={} #照片列表
        self.ht=htmltool.htmltool()
        self.curPath= self.ht.getPyFileDir()
        self.FileNum=0

    #设置urllib2 cookie
    def enableCookies(self):
        #建立一个cookies 容器
        self.cookies = cookielib.CookieJar()
        #将一个cookies容器和一个HTTP的cookie的处理器绑定
        cookieHandler = urllib2.HTTPCookieProcessor(self.cookies)
        #创建一个opener,设置一个handler用于处理http的url打开
        #self.opener = urllib2.build_opener(self.handler)
        httpHandler=urllib2.HTTPHandler(debuglevel=1)
        httpsHandler=urllib2.HTTPSHandler(debuglevel=1)
        self.opener = urllib2.build_opener(cookieHandler,httpHandler,httpsHandler)
        #安装opener，此后调用urlopen()时会使用安装过的opener对象
        urllib2.install_opener(self.opener)

    #获取当前时间
    def getJstime(self):
       itime= int(time.time() * 1000)
       return str(itime)

    #获取验证码
    def getRadomCode(self,repeat=2):
        '''
        -- js
        function chgRandomCode(ImgObj, randomCodeImgSrc) {
        ImgObj.src = randomCodeImgSrc+"?randomCodeType=emui4_login&_t=" + new Date().getTime();
        };
        -- http
        GET /casserver/randomcode?randomCodeType=emui4_login&_t=1462786575782 HTTP/1.1
        1462786575782
        1462796904193
        '''
        data =''
        ostime=self.getJstime()
        filename=self.curPath+'\\'+ostime+'.png'
        url= self.randomUrl+"?randomCodeType=emui4_login&_t="+ostime
        #print url
        try:
            request = urllib2.Request(url,headers=self.loginHeaders)
            response = urllib2.urlopen(request)
            data = response.read()
        except :
            time.sleep(5)
            print u'保存验证码图片[%s]出错，尝试:\n[%s]' %(url,2-repeat)
            if repeat>0:
                 return self.getRadomCode(repeat-1)
        if len(data)<= 0 : return
        f = open(filename, 'wb')
        f.write(data)
        #print u"保存图片:",fileName
        f.close()
        im = Image.open(filename)
        im.show()
        self.authcode=''
        self.authcode = raw_input(u'请输入4位验证码:')
        #删除验证码文件
        os.remove(filename)
        return

    def genLoginData(self,content):
        '''
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        11
        12

        '''
        tree = etree.HTML(content)
        form= tree.xpath('//div[@class="login-box"]')[0]
        #print len(form)
        params=OrderedDict()
        params['submit']=form.xpath('//*[@name="submit"]/@value')[0] #1
        params['loginUrl']= form.xpath('//*[@name="loginUrl"]/@value')[0]
        params['service'] = form.xpath('//*[@name="service"]/@value')[0]
        params['loginChannel']= form.xpath('//*[@name="loginChannel"]/@value')[0]
        params['reqClientType'] = form.xpath('//*[@name="reqClientType"]/@value')[0]
        params['deviceID']= form.xpath('//*[@name="deviceID"]/@value')[0]#6
        params['adUrl']= form.xpath('//*[@name="adUrl"]/@value')[0]
        params['lang'] = form.xpath('//*[@name="lang"]/@value')[0]
        params['inviterUserID']= form.xpath('//*[@name="inviterUserID"]/@value')[0]
        params['inviter'] = form.xpath('//*[@name="inviter"]/@value')[0]
        params['viewType']= form.xpath('//*[@name="viewType"]/@value')[0]#11
        params['quickAuth'] = form.xpath('//*[@name="quickAuth"]/@value')[0]
        params['userAccount']= self.username
        params['password'] = self.passwd
        params['authcode'] = self.authcode
        params=urllib.urlencode(params)
        return params

    def getLoginPage(self):
        request = urllib2.Request(self.loginUrl,headers=self.loginHeaders)
        response = urllib2.urlopen(request)
        page =''
        page= response.read()
        redUrl=response.geturl()
        return page.decode('utf-8')


    def checkUserPwd(self,postdata):
        '''
        #add header写法1
        request= urllib2.Request(self.checkpwdUrl,data)
        request.add_header('accept', 'application/json, text/javascript, */*');
        response = urllib2.urlopen(request)
        '''
        #add header写法2
        request = urllib2.Request(self.checkpwdUrl,postdata,headers=self.loginHeaders)
        response = urllib2.urlopen(request)
        rheader =''
        rheader = response.info()
        page= response.read()
        reUrl=response.geturl()
        return reUrl

    #调用正则表达式获取返回报文中的CSRFToken，成功返回1
    def getCSRFToken(self,page):
        '''







        '''
        self.CSRFToken=''
        pattern = re.compile('CSRFToken = "(.*?)"',re.S)
        #保存CSRFToken
        content = re.search(pattern,page)
        if content :
            self.CSRFToken = content.group(1)
            return '1'
        else:
            return '0'

    #打开相册页，获取CSRFToken字符，这个是关键字，在后续报文都将用到。
    def getAlbumPage(self):
        request=urllib2.Request(self.successUrl,headers=self.loginHeaders)
        response = urllib2.urlopen(request)
        rheader = response.info()
        page= response.read()
        redUrl=response.geturl()
        return self.getCSRFToken(page.decode('utf-8'))



    """
    Description : 将网页图片保存本地
    @param imgUrl : 待保存图片URL
    @param imgName : 待保存图片名称
    @return 无
    """
    def saveImage( self,imgUrl,imgName ="default.jpg" ):
        #使用requests的get方法直接下载文件，注意因为url是https，所以加了verify=False
        response = requests.get(imgUrl, stream=True,verify=False)
        image = response.content
        filename= imgName
        print("保存文件"+filename+"\n")
        try:
            with open(filename ,"wb") as jpg:
                jpg.write( image)
                return
        except IOError:
            print("IO Error\n")
            return
        finally:
            jpg.close

    """
    Description : 开启多线程执行下载任务,注意没有限制线程数
    @param filelist:待下载图片URL列表
    @return 无
    """
    def downFileMultiThread( self,urllist,namelist ):
        task_threads=[] #存储线程
        count=1
        i = 0
        for i in range(0,len(urllist)):
            fileurl = urllist[i]
            filename= namelist[i]
            t = threading.Thread(target=self.saveImage,args=(fileurl,filename))
            count = count+1
            task_threads.append(t)
        for task in task_threads:
            task.start()
        for task in task_threads:
            task.join()

    #多线程下载相册照片到目录 ,不同相册保存到不同的目录
    def downFileListMultiThread(self,dirname,hjsondata):
        if len(hjsondata)<= 0 : return 0
        hjson2 = {}
        hjson2 = json.loads(hjsondata)
        #新建目录，并切换到目录
        self.ht.mkdir(dirname)
        i = 0
        urllist=[]
        namelist=[]
        if hjson2.has_key("fileList"):
            for each in hjson2["fileList"]:
                urllist.append(hjson2["fileList"][i]["fileUrl"].encode('gbk'))
                namelist.append(hjson2["fileList"][i]["fileName"].encode('gbk'))
                self.FileNum += 1
                i += 1
                #每25个文件开始并发下载，并清空数组，或者最后一组
                if i%25==0 or i == len(hjson2["fileList"]):
                    self.downFileMultiThread(urllist,namelist)
                    urllist=[]
                    namelist=[]
        return i

    #下载相册照片到目录 ,不同相册保存到不同的目录
    def downFileList(self,dirname,hjsondata):
        if len(hjsondata)<= 0 : return
        hjson2 = {}
        hjson2 = json.loads(hjsondata)
        #新建目录，并切换到目录
        self.ht.mkdir(dirname)
        i = 0
        if hjson2.has_key("fileList"):
            for each in hjson2["fileList"]:
                self.saveImage(hjson2["fileList"][i]["fileUrl"].encode('gbk'),hjson2["fileList"][i]["fileName"].encode('gbk'))
                #每5个文件休息2秒
                self.FileNum += 1
                if i%5 ==0 : time.sleep(2)
                i += 1
        return i


    #保存相册照片地址到文件 ,不同相册保存到不同的文件
    def saveFileList2Txt(self,filename,hjsondata,flag):
        if len(hjsondata)<= 0 : return
        hjson2 = {}
        hjson2 = json.loads(hjsondata)
        lfilename = filename+u".txt"
        if flag == 0 : #新建文件
            print u'创建相册文件'+lfilename+"\n"
            #新建文件，代表新的相册重新开始计数
            self.FileNum = 0
            f = open(lfilename, 'wb')
        else: #追加文件
            f = open(lfilename, 'a')
        i = 0
        if hjson2.has_key("fileList"):
            for each in hjson2["fileList"]:
                f.write(hjson2["fileList"][i]["fileUrl"].encode('gbk')+"\n")
                #每一千行分页
                self.FileNum += 1
                if self.FileNum%1000 ==0 :f.write('\n\n\n\n\n\n--------------------page %s ------------------\n\n\n\n\n\n' %(int(self.FileNum/1000)))
                i += 1
        f.close()
        return i

    #循环读取相册文件
    def getFileList(self,hjsondata,parentkey,childkey):
        #step 3 getCoverFiles.action,循环取相册文件列表，单次最多取100条记录。
        #每次count都是最大数量49，不管实际数量是否够，每次currentnum递增，直到返回空列表。
        #albumIds[]=default-album-2&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=0&thumbType=imgcropa&fileType=0
        #albumIds[]=default-album-1&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=49&thumbType=imgcropa&fileType=0
        #albumIds[]=default-album-1&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=98&thumbType=imgcropa&fileType=0
        #albumIds[]=default-album-2&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=101&thumbType=imgcropa&fileType=0
        #最后一次返回 空列表
        #{"albumSortFlag":true,"code":0,"info":"success!","fileList":[]}
        #第一次取文件时，例如文件总数量只有2个，count也是放最大值49。
        #albumIds[]=default-album-102-220086000029851117&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=0&thumbType=imgcropa&fileType=0
        #[{u'photoNum': 2518, u'albumName': u'default-album-1', u'iversion': -1, u'albumId': u'default-album-1', u'flversion': -1, u'createTime': 1448065264550L, u'size': 0},
        #{u'photoNum': 100, u'albumName': u'default-album-2', u'iversion': -1, u'albumId': u'default-album-2', u'flversion': -1, u'createTime': 1453090781646L, u'size': 0}]
        hsjon={}
        hjson = json.loads(hjsondata.decode('utf-8'))
        paraAlbum=OrderedDict()
        if hjson.has_key(parentkey):
            for each in hjson[parentkey]:
                paraAlbum={}
                paraAlbum['albumIds[]'] = each[childkey]
                paraAlbum['ownerId'] = hjson['ownerId']
                paraAlbum['height'] = '300'
                paraAlbum['width'] = '300'
                paraAlbum['count'] = self.OnceMaxFile
                paraAlbum['thumbType'] = 'imgcropa'
                paraAlbum['fileType'] = '0'
                itotal= each['photoNum']
                icurrentnum=0
                while icurrentnum<itotal:
                    paraAlbum['currentNum'] = icurrentnum
                    paraAlbumstr = urllib.urlencode(paraAlbum)
                    request=urllib2.Request(self.getalbumfileUrl,headers=self.loginHeaders,data=paraAlbumstr)
                    response = urllib2.urlopen(request)
                    rheader = response.info()
                    page = response.read()
                    #调用gzip进行解压
                    if rheader.get('Content-Encoding')=='gzip':
                        data = StringIO.StringIO(page)
                        gz = gzip.GzipFile(fileobj=data)
                        page = gz.read()
                        gz.close()
                    page= page.decode('utf-8')
                    #print page.decode('utf-8')
                    #方案1：保存下载地址到文本文件中，但不下载文件
                    #icurrentnum += self.saveFileList2Txt(each[childkey],page,icurrentnum)
                    #方案2：单线程下载文件到本地
                    #icurrentnum += self.downFileList(each[childkey],page)
                    #方案3：多线程下载文件到本地
                    #unicode码格式
                    #print each[childkey].encode('gbk')
                    icurrentnum += self.downFileListMultiThread(each[childkey],page)
        return

    #step 1 getCloudAlbums,取相册列表
    def getAlbumList(self):
        self.loginHeaders={
        'Host': 'www.hicloud.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.hicloud.com',
        'X-Requested-With': 'XMLHttpRequest',
        'CSRFToken': self.CSRFToken,
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'DNT': '1',
        'Referer': 'https://www.hicloud.com/album',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        #self.loginHeaders={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        request=urllib2.Request(self.getalbumsUrl,headers=self.loginHeaders)
        response = urllib2.urlopen(request)
        page=''
        page= response.read()
        '''#返回报文
        {"ownerId":"220086000029851117","code":0,
        "albumList":[{"albumId":"default-album-1","albumName":"default-album-1","createTime":1448065264550,"photoNum":2521,"flversion":-1,"iversion":-1,"size":0},
                     {"albumId":"default-album-2","albumName":"default-album-2","createTime":1453090781646,"photoNum":101,"flversion":-1,"iversion":-1,"size":0}],
        "ownShareList":[{"ownerId":"220086000029851117","resource":"album","shareId":"default-album-102-220086000029851117","shareName":"微信","photoNum":2,"flversion":-1,"iversion":-1,"createTime":1448070407055,"source":"HUAWEI MT7-TL00","size":0,"ownerAcc":"jdstkxx@yeah.net","receiverList":[]}],
        "recShareList":[]}'
        '''
        if len(page)<=0 :
            print u'取相册列表出错，无返回报文!!!\n\n%s\n\n',page.decode('utf-8')
        return page

#主程序开始
hw=HuaWei()
hw.enableCookies()
count =0
while (count <3):
    count += 1
    content= hw.getLoginPage()
    if content == '' :
        print '获取登录信息出错，立即退出！！！\n\n[%s]\n\n' %(content)
        break
    #获取验证码
    hw.getRadomCode()
    #生成checkuserpwd提交时需要的POST data
    postdata=hw.genLoginData(content)
    #print postdata
    reUrl = hw.checkUserPwd(postdata)
    if reUrl.find("user_pwd_error") <> -1 :
        print u'用户名或用户密码错误，立即退出！！！\n\n[%s]\n\n' %(reUrl)
        break
    elif reUrl.find("random_code_error") <> -1 :
        print u'验证码错误，重试！！！\n\n[%s]\n\n' %(reUrl)
        continue
    else:
        print '恭喜恭喜，登录华为云成功！！！\n\n'
        iRet = hw.getAlbumPage()
        if iRet == 0 :
            print '打开相册页失败，未获取到CSRFToken！！！\n\n'
            break
        print '打开相册主页成功，获取到CSRFToken！！！\n\n'
        page = hw.getAlbumList()
        if page=='' :
            print '获取到相册列表失败！！！\n\n'
            break
        #保存相册列表
        hw.getFileList(page,'albumList','albumId')
        #保存公共相册列表
        hw.getFileList(page,'ownShareList','shareId')
        print '运行结束，可以用迅雷打开相册文件进行批量下载到本地！！！\n\n'

