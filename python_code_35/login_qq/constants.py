from login_qq.f2d import f2d # chrome复制的请求头字符串转字典
header1 = f2d('''
Accept: text/html, application/xhtml+xml, */*
Referer: https://mail.qq.com/
Accept-Language: zh-CN
User-Agent: Mozilla/5.0 (compatible; Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36; Windows NT 6.1; WOW64; Trident/5.0)
Host: xui.ptlogin2.qq.com
Connection: Keep-Alive''')

header2 = f2d('''
Accept: application/javascript, */*;q=0.8
Referer: https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/login?vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input24e6b9.css
Accept-Language: zh-CN
User-Agent: Mozilla/5.0 (compatible; Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36; Windows NT 6.1; WOW64; Trident/5.0)
Host: ssl.ptlogin2.qq.com
Connection: Keep-Alive''')

header3 = f2d('''
Accept: application/javascript, */*;q=0.8
Referer: https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/login?vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input24e6b9.css
Accept-Language: zh-CN
User-Agent: Mozilla/5.0 (compatible; Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36; Windows NT 6.1; WOW64; Trident/5.0)
Host: ssl.ptlogin2.qq.com
Connection: Keep-Alive''')

url1 = r'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/login?vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input24e6b9.css'
url2 = r'https://ssl.ptlogin2.qq.com/check?regmaster=&pt_tea=1&pt_vcode=0&uin={0[uname]}&appid=522005705&js_ver=10153&js_type=1&login_sig={0[login_sig]}&u1=https%3A%2F%2Fmail.qq.com%2Fcgi-bin%2Flogin%3Fvt%3Dpassport%26vm%3Dwpt%26ft%3Dloginpage%26target%3D&r={0[ran]}'
url3 = r'https://ssl.ptlogin2.qq.com/login?u={0[uname]}&verifycode={0[vcode]}&pt_vcode_v1=0&pt_verifysession_v1={0[pt_verifysession_v1]}&p={0[pwd]}&pt_randsalt=0&u1=https%3A%2F%2Fmail.qq.com%2Fcgi-bin%2Flogin%3Fvt%3Dpassport%26vm%3Dwpt%26ft%3Dloginpage%26target%3D%26account%3D2529640087&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=2-18-1464766263857&js_ver=10153&js_type=1&login_sig={0[login_sig]}&pt_uistyle=25&aid=522005705&daid=4&'

s1 = "'0','"
s2 = "','"

