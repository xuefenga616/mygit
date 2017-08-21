#coding:utf-8
__author__ = 'xuefeng'
import os,sys

basedir = '/'.join(os.path.dirname(__file__).split('/')[:-1])
sys.path.append(basedir)
from modules import main

if __name__ == '__main__':
    EntryPoint = main.ArgvHandler(sys.argv[1:])

