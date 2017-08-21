#coding:utf-8
__author__ = 'xuefeng'
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIND_HOST = '192.168.1.17'
BIND_PORT = 8080

ACCOUNT_DB = {
    'engine': 'file',
    'name': '%s/conf/accounts.json' %BASE_DIR,
}

USER_BASE_HOME_PATH = "%s/var/users"  %BASE_DIR