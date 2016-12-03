#coding:utf-8
__author__ = 'xuefeng'
import os,sys

basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)
sys.path.append('%s/BrightMonitor' %basedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'BrightMonitor.settings'
import django
django.setup()

import data_processing,trigger_handler
from redis_conn import RedisHelper as redis

class ManagementUtility(object):
    def __init__(self,argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.registered_actions = {
            'start': self.start,
            'stop': self.stop,
            'watch': self.watch,
        }

        self.argv_check()
    def argv_check(self):
        if len(self.argv) < 2:
            self.main_help_text()
        if self.argv[1] not in self.registered_actions:
            self.main_help_text()
        else:
            self.registered_actions[sys.argv[1]]()  #执行启动或其他命令
    def main_help_text(self):
        valid_commands = '''
        start   start monitor client
        stop    stop monitor client
        watch
        '''
        sys.exit(valid_commands)
    def start(self):
        print "going to start the monitor client"
        monitor_start = trigger_handler.TriggerHandler()
        monitor_start.start()
        reactor = data_processing.DataHandler(redis)
        reactor.looping()
    def stop(self):
        print "stopping the monitor client"
    def watch(self):
        trigger_watch = trigger_handler.TriggerHandler()
        trigger_watch.start_watching()
    def execute(self):
        pass

def execute_from_command_line(argv=None):
    utility = ManagementUtility(argv)
    utility.execute()

