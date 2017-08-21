#coding:utf-8
import requests
import hashlib
import re

def _md5(arg):
    obj = hashlib.md5()
    obj.update(arg)
    return obj.hexdigest()

url = "https://mp.weixin.qq.com/cgi-bin/bizlogin"
login_dict = {
    'username': 'xuefeng_11@qq.com',
    'pwd': _md5('123'),
    'imgcode': '',
    'f': 'json'
}
response = requests.post(url=url,data=login_dict,
                         headers={'Referer':"https://mp.weixin.qq.com/"})
print response.text

login_cookies = response.cookies.get_dict()
token = re.findall(".*token=(\d+)",response.text)[0]

Home_url = "https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN&token=" + token
home_response = requests.get(Home_url)
print home_response.text

