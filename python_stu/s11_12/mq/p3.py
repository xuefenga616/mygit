#coding:utf-8
__author__ = 'xuefeng'
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.12'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

#severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key='db',
                      body=message)
print(" [x] Sent %r" % (message))
connection.close()
