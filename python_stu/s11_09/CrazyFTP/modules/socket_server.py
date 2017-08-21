#coding:utf-8
__author__ = 'xuefeng'
import SocketServer
import json,os
from auth import authentication
from conf import settings
import hashlib  #md5

class FtpServer(SocketServer.BaseRequestHandler):
    response_code = {
        '200': 'User password authentication!',
        '201': 'Invalid username or password',
        '202': 'User expired.',
        '300': 'File ready to send',
        '301': 'File ready to recv',
    }
    def handle(self):
        print self.client_address
        shutdown_flag = False
        while not shutdown_flag:
            data = self.request.recv(1024)
            self.data_parser(data)  #先验证用户，再干活：cmd__get
    def data_parser(self,data):
        data = json.loads(data)
        if data.get("action"):  #有action这个key
            action_type = data.get("action")
            if hasattr(self,action_type):
                func = getattr(self,action_type)
                func(data)
            else:
                print "invalid action type ",data
        else:   #invalid data stuctor
            print "invalid client data ",data
    def user_auth(self,data):
        username = data.get("username")
        password = data.get("password")
        print "===>got here...",username,password

        auth_status,auth_msg = authentication(username,password)
        if auth_status is True:
            print "authentication successful ..."
            response_data = {'status':'200','data':[]}
            self.login_user = username  #加个类变量，用以验证是这个用户登录成功了
            self.home_path = "%s/%s" %(settings.USER_BASE_HOME_PATH,self.login_user)
        else:
            print "authentication failed ..."
            response_data = {'status':'201','data':[]}

        self.request.send(json.dumps(response_data))    #发给客户端相关状态码
    def cmd__get(self,data):
        print "----client ask for downloading data",data
        if hasattr(self,'login_user'):  #证明已经登录了
            filename_path = data.get('filename')
            file_with_abs_path = "%s/%s" %(self.home_path,filename_path)
            print file_with_abs_path
            if os.path.isfile(file_with_abs_path):  #如果存在此文件
                file_size = os.path.getsize(file_with_abs_path)
                response_data = {"status":"300",
                                 "data":[{"filename":filename_path,"size":file_size}]
                                 }
                self.request.send(json.dumps(response_data))

                client_response = json.loads(self.request.recv(1024))   #等客户端的回应
                if client_response.get('status') == "301":
                    f = file(file_with_abs_path,"rb")
                    file_md5 = hashlib.md5()    #生成md5对象,md5值进行文件校验
                    send_size = 0
                    while file_size != send_size:
                        one_data = f.read(4096)     #一次发4096
                        self.request.send(one_data)
                        send_size += len(one_data)
                        file_md5.update(one_data)
                        print file_size,", ",send_size
                    else:
                        md5_str = file_md5.hexdigest()  #生成最终md5值
                        print "\033[32;1m send file done\033[0m"
                        print "\033[32;1m---file md5 [%s]---\033[0m" %md5_str

                        f.close()








