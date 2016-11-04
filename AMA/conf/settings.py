#coding:utf-8

import sys

DATABASE = {
    'host': '127.0.0.1',
    'port': 3306,
    'db_name': 'ama',
    'username': 'root',
    'password': '123456',
}

MaxTaskProcesses = 4

Welcome_msg = '''
|----------\033[32;1m[Welcome login Auditing server]\033[0m-----------|
|            Version :   0.1                         |
|            Author  :   xuefeng                     |
|            Email:      xuefeng16@huawei.com        |
|----------------------------------------------------|\n\n'''

DatabaseInitSqlFile = 'src/audit.sql'