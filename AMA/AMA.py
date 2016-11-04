#coding:utf-8

import sys

basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)

from core import main

if __name__ == '__main__':
    main.call(sys.argv[1:])