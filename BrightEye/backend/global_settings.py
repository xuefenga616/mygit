#coding:utf-8
__author__ = 'Administrator'

import os,sys


base_dir = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
#print base_dir
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BrightEye.settings")

from web import models
