#coding:utf-8
__author__ = 'Administrator'
import smtplib

From = "xuefeng_11@qq.com"
From_pass = input("请输入密码")
Host = "smtp.qq.com"
To = "xuefeng_11@qq.com"
Subject = "Mail"

text = "This is a test mail!"
string = (
    "From: %s" %From,
    "To: %s" %To,
    "Subject: %s" %Subject,
    "",
    text,
    )
Body = '\r\n'.join(string)
server = smtplib.SMTP_SSL(Host,465)
server.login(From,From_pass)
server.sendmail(From,[To],Body)
server.quit()


