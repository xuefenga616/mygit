#coding:utf-8

import sys,os
import mysql_conn
from modules import demo
from conf import settings
import commands
import getpass

def call(sys_args):

    if len(sys_args) == 0:
        feature_list()
    else:
        feature_ins = Features()
        if hasattr(feature_ins, sys_args[0]):
            func = getattr(feature_ins,sys_args[0])
            func(sys_args)
        else:
            print "\033[31;1mInvalid argument!\033[0m"
            feature_list()
def feature_list():
    features = '''
    run     run audit interactive interface
    init    create audit database tables
            --with_sample_data create audit database tables with sample data
    manage  management interface for administrator
    help    show helps
    '''
    print(features)
class Features(object):
    def __init__(self):
        pass

    def run(self,argv):
        self.ms = mysql_conn.MysqlConn()
        if self.__auth(self.ms):
            print settings.Welcome_msg
            self.__user_interactive()
    def __user_interactive(self):
        self.fetch_hosts()
    def fetch_hosts(self):
        host_user_info = self.ms.select("select username,password from host_users where id=1")[0]
        host_info = self.ms.select("select hostname,ip from hosts")
        host_info_list = []
        for i in range(len(host_info)):
            id = i + 1
            tmp_dic = {
                'id': id,
                'hostname':host_info[i][0],
                'ip':host_info[i][1],
                'username': host_user_info[0],
                'password': host_user_info[1],
                'port': 22,
            }
            print tmp_dic['id'],tmp_dic['hostname'],tmp_dic['ip']
            host_info_list.append(tmp_dic)
        #print host_info_list

        user_choice = raw_input("\033[32;1m Please choice:\033[0m").strip()
        while True:
            if len(user_choice) == 0:
                continue
            if user_choice.isdigit() and int(user_choice) <= len(host_info):
                for tmp_dic2 in host_info_list:
                    if tmp_dic2['id'] == int(user_choice):
                        print "That's right!"
                        try:
                            demo.login(
                                self,
                                tmp_dic2['ip'],
                                tmp_dic2['port'],
                                tmp_dic2['username'],
                                tmp_dic2['password'])
                        except Exception,e:
                            print "\033[31;1m %s\033[0m" %e
                return True
            else:
                sys.exit("Bye!")


    def __auth(self,mysql_conn):
       cnt = 0
       while cnt < 3:
            user = raw_input("Username:").strip()
            passwd = getpass.getpass("Password:")
            if len(user) == 0 or len(passwd) == 0:
                print "Username or password cannot be empty!"
                continue
            user_in_db  = mysql_conn.select("select * from user where username=%s and password=%s",(user,passwd))
            if len(user_in_db) > 0:
                self.login_user = user
                return True
            else:
                print "\033[31;1m Invalid username or password!\033[0m"
                cnt +=1
       sys.exit("Invalid username and password, too many attempts, exit.")
    def flush_audit_log(self,log_list):
        query_code = "insert into audit_log (user,ip,host_user,cmd,date) values(%s,%s,%s,%s,%s)"
        execute_status = self.ms.insert_many(query_code,log_list)
        if execute_status:
            return True

    def init(self,msg):
        '''create database tables'''
        print '-->',msg
        base_dir ='/'.join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
        db_file = '%s/%s' %(base_dir,settings.DatabaseInitSqlFile)
        #if '--with_sample_data' in msg:
        #    db_file = '%s/%s' %(base_dir,settings.DatabaseInitSqlFileWithSample)

        restore_cmd = "mysql -u%s -p%s -h%s %s <%s" %(settings.DATABASE['username'],
                                                      settings.DATABASE['password'],
                                                      settings.DATABASE['host'],
                                                      settings.DATABASE['db_name'],
                                                      db_file
                                                      )

        exec_res = commands.getstatusoutput(restore_cmd)