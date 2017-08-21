#coding:utf-8
__author__ = 'xuefeng'
import pika
import time

conn = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.1.12"))
chan = conn.channel()

chan.queue_declare(queue="fm107.8",durable=True)

def callback(ch,method,properties,body):
    print " [x] Received %r" %body      # %r是给字符串加单引号
    time.sleep(10)
    #print "Ok"
    ch.basic_ack(delivery_tag=method.delivery_tag)

chan.basic_consume(callback,
                   queue="fm107.8",
                   no_ack=False)
print " [*] Waiting for messages. To exit press Ctrl+C"
chan.start_consuming()
