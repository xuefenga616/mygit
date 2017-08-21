#coding:utf-8
__author__ = 'xuefeng'
"""
rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
yum -y install erlang
yum -y install rabbitmq-server
service rabbitmq-server start/stop
"""

import pika
import sys

conn = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.12'))
chan = conn.channel()

chan.exchange_declare(exchange='logs',type='fanout')    #发布订阅模式

msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
chan.basic_publish(exchange='logs',
                   routing_key="",
                   body=msg,
                   )
print "[x] Sent %r" %msg
conn.close()