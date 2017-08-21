#coding:utf-8
__author__ = 'xuefeng'
"""
rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
yum -y install erlang
yum -y install rabbitmq-server
service rabbitmq-server start/stop
"""

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.12'))
chan = conn.channel()

chan.queue_declare(queue="fm107.8",durable=True)   #声明一个队列，durable=True表示持久化存储

chan.basic_publish(exchange='',
                   routing_key="fm107.8",
                   body="Hello world!",
                   properties=pika.BasicProperties(delivery_mode=2)     #代表此条消息持久化
                   )
print "[x] Sent 'Hello world!'"
conn.close()