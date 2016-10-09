#_*_coding:utf-8_*_
from linux import *
def avg(mins,operator,data):
    print 'run------avg-----',mins,operator, data
    avg_value = sum(data)/len(data)
    print avg_value

    if operator == 'gt':
        pass
    elif operator == 'lt':
        pass


def last(mins,operator,data):
    print 'run------last-----',mins,operator, data
def hit(mins,operator,data):
    print 'run------hit-----',mins,operator, data


