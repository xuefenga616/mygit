#coding:utf-8
__author__ = 'xuefeng'
import os,sys,socket,json
import time,hashlib

class FTPClient(object):
    def __init__(self,argv):
        self.args = argv
        print self.args
        self.response_code = {
            '200': 'User password authentication!',
            '201': 'Invalid username or password',
            '202': 'User expired.',
            '300': 'File ready to send',
            '301': 'File ready to recv',
        }
        self.parse_argv()
        self.handle()
    def parse_argv(self):
        if len(self.args) < 4:
            self.help_msg()
        else:
            mandatory_fields = ["-s","-p"]
            for i in mandatory_fields:
                if i not in self.args:
                    sys.exit("The argument [%s] is mandatory!" %i)
            try:
                self.ftp_host = self.args[self.args.index("-s") + 1]
                self.ftp_port = int(self.args[self.args.index("-p") + 1])
            except (IndexError,ValueError) as e:
                print "\033[31;1m%s\033[0m" %e
                self.help_msg()
    def help_msg(self):
        help_msg = '''
        -s ftp_server_addr      :the ftp server you want to connect
        -p ftp_port             :ftp port
        '''
        sys.exit(help_msg)
    def connect(self,host,port):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((host,port))
        except socket.error as e:
            sys.exit(e)
    def handle(self):
        self.connect(self.ftp_host,self.ftp_port)
        if self.auth():
            self.interactive()  #现在就可以和服务器端交互了
    def interactive(self):
        quit_flag = False
        while not quit_flag:
            user_input = raw_input("\033[32;1m%s\033[0m [%s]:" %(self.user,self.cwd)).strip()
            if len(user_input) == 0:
                continue
            self.cmd_parser(user_input)     #支持上传、下载、ls
    def cmd_parser(self,user_input):
        cmd_list = user_input.split()
        if hasattr(self,"cmd__"+cmd_list[0]):
            func = getattr(self,"cmd__"+cmd_list[0])
            func(cmd_list[1:])
        else:
            print "\033[31;1m Invalid cmd\033[0m"
    def cmd__get(self,cmd_list):
        if len(cmd_list) < 1:
            print "\033[31;1m remote filename is specifiled\033[0m"
        else:
            remote_filename = cmd_list[0]
            msg_str = {"action":"cmd__get",
                       "filename": remote_filename,
                       }
            self.sock.send(json.dumps(msg_str))     #第二波的第一次
            server_response = json.loads(self.sock.recv(1024))  #接收返回数据:response = {"status": "300",data: [{"filename":"test.txt","size":3333}]}
            if server_response.get('status') == "300":
                # file exist, and ready to send
                total_file_size = int(server_response['data'][0].get('size'))
                client_response = {"action":"cmd__get",
                                   "filename": remote_filename,
                                   "status": "301"
                                   }
                self.sock.send(json.dumps(client_response))     #第二波的第二次

                received_size = 0
                local_filename = os.path.basename(remote_filename)
                tmp_f = open(local_filename,"wb")

                file_md5 = hashlib.md5()    #生成md5对象,md5值进行文件校验
                while total_file_size != received_size: #代表没收完
                    data = self.sock.recv(4096)
                    #print total_file_size,", ",received_size
                    received_size += len(data)
                    tmp_f.write(data)
                    file_md5.update(data)
                    #设置进度条
                    progress_num = received_size * 100 / total_file_size    #总共需要打印的进度条#的个数
                    sys.stdout.write("\r%s%% " %progress_num + "#"*progress_num)
                    sys.stdout.flush()
                    #time.sleep(0.01)
                else:
                    md5_str = file_md5.hexdigest()  #生成最终md5值
                    print "\033[32;1m---file download success---\033[0m"
                    print "\033[32;1m---file md5 [%s]---\033[0m" %md5_str
                    tmp_f.close()


    def auth(self):
        retry_count = 0
        while retry_count < 3:
            username = raw_input("Username:").strip()
            if len(username) == 0:
                continue
            password = raw_input("Password:").strip()
            if len(password) == 0:
                continue
            data = {
                "username":username,
                "password":password,
                "action": "user_auth"
            }
            cmd_str = json.dumps(data)
            self.sock.send(cmd_str)     #把个人信息发给服务端，服务端验证后返回
            server_response = json.loads(self.sock.recv(1024))
            #eg: {"status":200, "data":[]}
            if server_response["status"] == "200":
                print self.response_code["200"]
                self.user = username
                self.cwd = "/"  #设置当前路径
                return True
            else:
                print self.response_code[server_response["status"]]
                retry_count += 1
        else:
            sys.exit("\033[31;1m Too many attempts!\033[0m")
