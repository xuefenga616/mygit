#coding:utf-8
__author__ = 'xuefeng'

import os,sys

base_dir = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    client = main.command_handler(sys.argv)
