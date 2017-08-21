#coding:utf-8
import urllib2
import json
import cookielib


def urllib2_request(url, method="GET", cookie="", headers={}, data=None):
    """
    :param url: 要请求的url
    :param cookie: 请求方式，GET、POST、DELETE、PUT..
    :param cookie: 要传入的cookie，cookie= 'k1=v1;k1=v2'
    :param headers: 发送数据时携带的请求头，headers = {'ContentType':'application/json; charset=UTF-8'}
    :param data: 要发送的数据GET方式需要传入参数，data={'d1': 'v1'}
    :return: 返回元祖，响应的字符串内容 和 cookiejar对象
    对于cookiejar对象，可以使用for循环访问：
        for item in cookiejar:
            print item.name,item.value
    """
    if data:
        data = json.dumps(data)

    cookie_jar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(handler)
    opener.addheaders.append(['Cookie', 'k1=v1;k1=v2'])
    request = urllib2.Request(url=url, data=data, headers=headers)
    request.get_method = lambda: method

    response = opener.open(request)
    origin = response.read()

    return origin, cookie_jar


# GET
# result = urllib2_request('http://127.0.0.1:8000/login/', method="GET")
# print result[0]
# print result[1]

# POST
result = urllib2_request(
    'http://127.0.0.1:8000/login/',  method="POST",
    data= {
        'k1':'v1',
        'csrfmiddlewaretoken':'JxRCIv5Y2JHIyXkE1JhoCbfCfUNz5wPxMPcE3IUJQqG0NLoMxUsnK6GikcpEGc1s'
    }
)

# PUT
# result = urllib2_request('http://127.0.0.1:8000/index/',  method="PUT", data= {'k1': 'v1'})

