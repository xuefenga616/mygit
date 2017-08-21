#coding:utf-8
__author__ = 'xuefeng'
import paramiko
import os,sys
import select
import socket
import termios,tty

tran = paramiko.Transport(('192.168.1.11',22))
tran.start_client()
default_path = os.path.join(os.environ['HOME'],'.ssh','id_rsa')
key = paramiko.RSAKey.from_private_key_file(default_path)
tran.auth_publickey('root',key)

#打开一个通道
chan = tran.open_session()
#获取一个终端
chan.get_pty()
#激活器
chan.invoke_shell()

f = open('/tmp/record.txt','w')
# 获取原tty属性
oldtty = termios.tcgetattr(sys.stdin)
try:
    # 为tty设置新属性
    # 默认当前tty设备属性：
    #   输入一行回车，执行
    #   CTRL+C 进程退出，遇到特殊字符，特殊处理。

    # 这是为原始模式，不认识所有特殊符号
    # 放置特殊字符应用在当前终端，如此设置，将所有的用户输入均发送到远程服务器
    tty.setraw(sys.stdin.fileno())
    chan.settimeout(0.0)

    while True:
        # 监视 用户输入 和 远程服务器返回数据（socket）
        # 阻塞，直到句柄可读
        r, w, e = select.select([chan, sys.stdin], [], [], 1)
        if chan in r:
            try:
                x = chan.recv(1024)
                if len(x) == 0:
                    print '\r\n*** EOF\r\n',
                    f.close()
                    break
                sys.stdout.write(x)
                sys.stdout.flush()
            except socket.timeout:
                pass
        if sys.stdin in r:
            x = sys.stdin.read(1)
            if len(x) == 0:
                break
            if x == '\t':
                pass
            else:
                f.write(x)
            chan.send(x)

finally:
    # 重新设置终端属性
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
    pass


chan.close()
tran.close()