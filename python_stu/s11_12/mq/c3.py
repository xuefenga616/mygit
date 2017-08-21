#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.12'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# severities = sys.argv[1:]
# if not severities:
#     sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
#     sys.exit(1)
#
# for severity in severities:
#     channel.queue_bind(exchange='direct_logs',
#                        queue=queue_name,
#                        routing_key=severity)

channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key='dali')
channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key='db')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % (body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
