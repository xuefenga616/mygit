#coding:utf-8
__author__ = 'xuefeng'
import pika
import time

conn = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.1.12"))
chan = conn.channel()

chan.exchange_declare(exchange='logs',type='fanout')

result = chan.queue_declare(exclusive=True)
queue_name = result.method.queue

chan.queue_bind(exchange='logs',queue=queue_name)

print " [*] Waiting for logs. To exit press Ctrl+C"

def callback(ch,method,properties,body):
    print " [x] Received %r" %body      # %r是给字符串加单引号

chan.basic_consume(callback,
                   queue=queue_name,
                   no_ack=True)

chan.start_consuming()
