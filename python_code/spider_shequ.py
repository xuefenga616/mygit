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
    #��Ϊ�Ʒ����¼
    '''
    ����http://www.hicloud.com ִ�жಽ��ת
    1����ֱ����ҳ����refresh��ת��http://www.hicloud.com/others/login.action
    2����ֱ��redirect��https://hwid1.vmall.com/casserver/logout?service=https://www.hicloud.com:443/logout
    3����redirect��https://hwid1.vmall.com/casserver/remoteLogin?service=https://www.hicloud.com:443/others/login.action&loginChannel=1000002&reqClientType=1&loginUrl=https://hwid1.vmall.com/oauth2/account/login?reqClientType=1&lang=zh-cn&adUrl=https://www.hicloud.com:443/others/show_advert.action
    4����redirect��https://hwid1.vmall.com/oauth2/account/login?reqClientType=1&validated=true&service=https://www.hicloud.com:443/others/login.action&loginChannel=1000002&reqClientType=1&adUrl=https://www.hicloud.com:443/others/show_advert.action&lang=zh-cn
    ������ӻ�ˢ�³�����¼���棬������ֱ��ʹ������4���е�½��
    5��������4�а���һ��ˢ����֤���request: https://hwid1.vmall.com/casserver/randomcode?randomCodeType=emui4_login&_t=1462786575782
    6������������https://hwid1.vmall.com/casserver/remoteLogin����post�ύ
    7����¼�ɹ�����ٴ�ִ��3��redirect���ֱ���:
    https://www.hicloud.com:443/others/login.action?lang=zh-cn&ticket=1ST-157502-OVRaMo6aV9BcM9Sh2Dpe-cas
    https://www.hicloud.com:443/others/login.action?lang=zh-cn
    https://www.hicloud.com:443/home
    ���ǵ�¼ʧ�ܣ���redirect������4����˱���ֱ��ʹ������4���е�¼��
    https://hwid1.vmall.com/oauth2/account/login?validated=true&errorMessage=random_code_error|user_pwd_continue_error&service=https%3A%2F%2Fwww.hicloud.com%3A443%2Fothers%2Flogin.action%3Flang%3Dzh-cn&loginChannel=1000002&reqClientType=1&adUrl=https%3A%2F%2Fwww.hicloud.com%3A443%2Fothers%2Fshow_advert.action%3Flang%3Dzh-cn&lang=zh-cn&viewT
    '''

    def __init__(self):
        self.username='13544270030' #�û���
        self.passwd='Xf19850917' #�û�����
        self.authcode='' #��֤��
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
        self.OnceMaxFile=100 #��������ȡ�ļ�����
        self.FileList={} #��Ƭ�б�
        self.ht=htmltool.htmltool()
        self.curPath= self.ht.getPyFileDir()
        self.FileNum=0

    #����urllib2 cookie
    def enableCookies(self):
        #����һ��cookies ����
        self.cookies = cookielib.CookieJar()
        #��һ��cookies������һ��HTTP��cookie�Ĵ�������
        cookieHandler = urllib2.HTTPCookieProcessor(self.cookies)
        #����һ��opener,����һ��handler���ڴ���http��url��
        #self.opener = urllib2.build_opener(self.handler)
        httpHandler=urllib2.HTTPHandler(debuglevel=1)
        httpsHandler=urllib2.HTTPSHandler(debuglevel=1)
        self.opener = urllib2.build_opener(cookieHandler,httpHandler,httpsHandler)
        #��װopener���˺����urlopen()ʱ��ʹ�ð�װ����opener����
        urllib2.install_opener(self.opener)

    #��ȡ��ǰʱ��
    def getJstime(self):
       itime= int(time.time() * 1000)
       return str(itime)

    #��ȡ��֤��
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
            print u'������֤��ͼƬ[%s]��������:\n[%s]' %(url,2-repeat)
            if repeat>0:
                 return self.getRadomCode(repeat-1)
        if len(data)<= 0 : return
        f = open(filename, 'wb')
        f.write(data)
        #print u"����ͼƬ:",fileName
        f.close()
        im = Image.open(filename)
        im.show()
        self.authcode=''
        self.authcode = raw_input(u'������4λ��֤��:')
        #ɾ����֤���ļ�
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
        #add headerд��1
        request= urllib2.Request(self.checkpwdUrl,data)
        request.add_header('accept', 'application/json, text/javascript, */*');
        response = urllib2.urlopen(request)
        '''
        #add headerд��2
        request = urllib2.Request(self.checkpwdUrl,postdata,headers=self.loginHeaders)
        response = urllib2.urlopen(request)
        rheader =''
        rheader = response.info()
        page= response.read()
        reUrl=response.geturl()
        return reUrl

    #����������ʽ��ȡ���ر����е�CSRFToken���ɹ�����1
    def getCSRFToken(self,page):
        '''







        '''
        self.CSRFToken=''
        pattern = re.compile('CSRFToken = "(.*?)"',re.S)
        #����CSRFToken
        content = re.search(pattern,page)
        if content :
            self.CSRFToken = content.group(1)
            return '1'
        else:
            return '0'

    #�����ҳ����ȡCSRFToken�ַ�������ǹؼ��֣��ں������Ķ����õ���
    def getAlbumPage(self):
        request=urllib2.Request(self.successUrl,headers=self.loginHeaders)
        response = urllib2.urlopen(request)
        rheader = response.info()
        page= response.read()
        redUrl=response.geturl()
        return self.getCSRFToken(page.decode('utf-8'))



    """
    Description : ����ҳͼƬ���汾��
    @param imgUrl : ������ͼƬURL
    @param imgName : ������ͼƬ����
    @return ��
    """
    def saveImage( self,imgUrl,imgName ="default.jpg" ):
        #ʹ��requests��get����ֱ�������ļ���ע����Ϊurl��https�����Լ���verify=False
        response = requests.get(imgUrl, stream=True,verify=False)
        image = response.content
        filename= imgName
        print("�����ļ�"+filename+"\n")
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
    Description : �������߳�ִ����������,ע��û�������߳���
    @param filelist:������ͼƬURL�б�
    @return ��
    """
    def downFileMultiThread( self,urllist,namelist ):
        task_threads=[] #�洢�߳�
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

    #���߳����������Ƭ��Ŀ¼ ,��ͬ��ᱣ�浽��ͬ��Ŀ¼
    def downFileListMultiThread(self,dirname,hjsondata):
        if len(hjsondata)<= 0 : return 0
        hjson2 = {}
        hjson2 = json.loads(hjsondata)
        #�½�Ŀ¼�����л���Ŀ¼
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
                #ÿ25���ļ���ʼ�������أ���������飬�������һ��
                if i%25==0 or i == len(hjson2["fileList"]):
                    self.downFileMultiThread(urllist,namelist)
                    urllist=[]
                    namelist=[]
        return i

    #���������Ƭ��Ŀ¼ ,��ͬ��ᱣ�浽��ͬ��Ŀ¼
    def downFileList(self,dirname,hjsondata):
        if len(hjsondata)<= 0 : return
        hjson2 = {}
        hjson2 = json.loads(hjsondata)
        #�½�Ŀ¼�����л���Ŀ¼
        self.ht.mkdir(dirname)
        i = 0
        if hjson2.has_key("fileList"):
            for each in hjson2["fileList"]:
                self.saveImage(hjson2["fileList"][i]["fileUrl"].encode('gbk'),hjson2["fileList"][i]["fileName"].encode('gbk'))
                #ÿ5���ļ���Ϣ2��
                self.FileNum += 1
                if i%5 ==0 : time.sleep(2)
                i += 1
        return i


    #���������Ƭ��ַ���ļ� ,��ͬ��ᱣ�浽��ͬ���ļ�
    def saveFileList2Txt(self,filename,hjsondata,flag):
        if len(hjsondata)<= 0 : return
        hjson2 = {}
        hjson2 = json.loads(hjsondata)
        lfilename = filename+u".txt"
        if flag == 0 : #�½��ļ�
            print u'��������ļ�'+lfilename+"\n"
            #�½��ļ��������µ�������¿�ʼ����
            self.FileNum = 0
            f = open(lfilename, 'wb')
        else: #׷���ļ�
            f = open(lfilename, 'a')
        i = 0
        if hjson2.has_key("fileList"):
            for each in hjson2["fileList"]:
                f.write(hjson2["fileList"][i]["fileUrl"].encode('gbk')+"\n")
                #ÿһǧ�з�ҳ
                self.FileNum += 1
                if self.FileNum%1000 ==0 :f.write('\n\n\n\n\n\n--------------------page %s ------------------\n\n\n\n\n\n' %(int(self.FileNum/1000)))
                i += 1
        f.close()
        return i

    #ѭ����ȡ����ļ�
    def getFileList(self,hjsondata,parentkey,childkey):
        #step 3 getCoverFiles.action,ѭ��ȡ����ļ��б��������ȡ100����¼��
        #ÿ��count�����������49������ʵ�������Ƿ񹻣�ÿ��currentnum������ֱ�����ؿ��б�
        #albumIds[]=default-album-2&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=0&thumbType=imgcropa&fileType=0
        #albumIds[]=default-album-1&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=49&thumbType=imgcropa&fileType=0
        #albumIds[]=default-album-1&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=98&thumbType=imgcropa&fileType=0
        #albumIds[]=default-album-2&ownerId=220086000029851117&height=300&width=300&count=49&currentNum=101&thumbType=imgcropa&fileType=0
        #���һ�η��� ���б�
        #{"albumSortFlag":true,"code":0,"info":"success!","fileList":[]}
        #��һ��ȡ�ļ�ʱ�������ļ�������ֻ��2����countҲ�Ƿ����ֵ49��
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
                    #����gzip���н�ѹ
                    if rheader.get('Content-Encoding')=='gzip':
                        data = StringIO.StringIO(page)
                        gz = gzip.GzipFile(fileobj=data)
                        page = gz.read()
                        gz.close()
                    page= page.decode('utf-8')
                    #print page.decode('utf-8')
                    #����1���������ص�ַ���ı��ļ��У����������ļ�
                    #icurrentnum += self.saveFileList2Txt(each[childkey],page,icurrentnum)
                    #����2�����߳������ļ�������
                    #icurrentnum += self.downFileList(each[childkey],page)
                    #����3�����߳������ļ�������
                    #unicode���ʽ
                    #print each[childkey].encode('gbk')
                    icurrentnum += self.downFileListMultiThread(each[childkey],page)
        return

    #step 1 getCloudAlbums,ȡ����б�
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
        '''#���ر���
        {"ownerId":"220086000029851117","code":0,
        "albumList":[{"albumId":"default-album-1","albumName":"default-album-1","createTime":1448065264550,"photoNum":2521,"flversion":-1,"iversion":-1,"size":0},
                     {"albumId":"default-album-2","albumName":"default-album-2","createTime":1453090781646,"photoNum":101,"flversion":-1,"iversion":-1,"size":0}],
        "ownShareList":[{"ownerId":"220086000029851117","resource":"album","shareId":"default-album-102-220086000029851117","shareName":"΢��","photoNum":2,"flversion":-1,"iversion":-1,"createTime":1448070407055,"source":"HUAWEI MT7-TL00","size":0,"ownerAcc":"jdstkxx@yeah.net","receiverList":[]}],
        "recShareList":[]}'
        '''
        if len(page)<=0 :
            print u'ȡ����б�����޷��ر���!!!\n\n%s\n\n',page.decode('utf-8')
        return page

#������ʼ
hw=HuaWei()
hw.enableCookies()
count =0
while (count <3):
    count += 1
    content= hw.getLoginPage()
    if content == '' :
        print '��ȡ��¼��Ϣ���������˳�������\n\n[%s]\n\n' %(content)
        break
    #��ȡ��֤��
    hw.getRadomCode()
    #����checkuserpwd�ύʱ��Ҫ��POST data
    postdata=hw.genLoginData(content)
    #print postdata
    reUrl = hw.checkUserPwd(postdata)
    if reUrl.find("user_pwd_error") <> -1 :
        print u'�û������û�������������˳�������\n\n[%s]\n\n' %(reUrl)
        break
    elif reUrl.find("random_code_error") <> -1 :
        print u'��֤��������ԣ�����\n\n[%s]\n\n' %(reUrl)
        continue
    else:
        print '��ϲ��ϲ����¼��Ϊ�Ƴɹ�������\n\n'
        iRet = hw.getAlbumPage()
        if iRet == 0 :
            print '�����ҳʧ�ܣ�δ��ȡ��CSRFToken������\n\n'
            break
        print '�������ҳ�ɹ�����ȡ��CSRFToken������\n\n'
        page = hw.getAlbumList()
        if page=='' :
            print '��ȡ������б�ʧ�ܣ�����\n\n'
            break
        #��������б�
        hw.getFileList(page,'albumList','albumId')
        #���湫������б�
        hw.getFileList(page,'ownShareList','shareId')
        print '���н�����������Ѹ�״�����ļ������������ص����أ�����\n\n'

