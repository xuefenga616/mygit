#coding:utf-8
__author__ = 'xuefeng'
import os,sys

basedir = '/'.join(os.path.dirname(__file__).split('/')[:-1])
sys.path.append(basedir)
from modules import socket_client

if __name__ == '__main__':
    sock_cli = socket_client.FTPClient(sys.argv[1:])
