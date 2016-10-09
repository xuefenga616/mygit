#coding:utf-8
import requests
import random
import constants #常量文件,urls,headers,字符串等等.
import encryption #加密算法
import wbqzj #取中间文本
from hidepass import pwd_input #星号密码

uname = input('QQ号:')
pwd = pwd_input('密码:')
    
sesh = requests.Session()

# 获取登录需要的数据
sesh.headers.update(constants.header1)
url = constants.url1
res = sesh.get(url)

# 获取验证码
sesh.headers.update(constants.header2)
login_sig = res.cookies['pt_login_sig']
ran = random.random()
url = constants.url2.format(vars())
res = sesh.get(url)

# 登录
sesh.headers.update(constants.header3)
vcode = wbqzj.qwb(res.text, constants.s1, constants.s2)
if len(vcode) != 4:
    pass # 需要验证码的部分,一般自己的q不用,以后有时间再写
pwd = encryption.getEncryption(pwd, uname, vcode)
pt_verifysession_v1 = res.cookies['ptvfsession']
url = constants.url3.format(vars())

res = sesh.get(url)
print(res.text)
input()

