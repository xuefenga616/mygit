#coding:utf-8
__author__ = 'Administrator'
import os,sys

BaseDir = "\\".join(os.path.dirname(os.path.abspath(__file__)).split("\\")[:-2])
#print BaseDir
sys.path.append(BaseDir)    #把路径加到环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE","MyOPS.settings")
from hosts import models
import django

from django.core.exceptions import ObjectDoesNotExist
import multiprocessing  #使用多进程
import paramiko_handle

django.setup()  #外部脚本调用django.db

def by_paramiko(task_id):
    try:
        task_obj = models.TaskLog.objects.get(id=task_id)
        pool = multiprocessing.Pool(processes=2)    #使用进程池

        res = []
        if task_obj.task_type == 'multi_cmd':
            for h in task_obj.hosts.select_related():   #hosts = models.ManyToManyField('BindHostToUser')
                p = pool.apply_async(paramiko_handle.paramiko_ssh,args=(task_id,h,task_obj.cmd))
                res.append(p)
        elif task_obj.task_type in ('file_send','file_get'):
            for h in task_obj.hosts.select_related():   #hosts = models.ManyToManyField('BindHostToUser')
                p = pool.apply_async(paramiko_handle.paramiko_sftp,args=(task_id,h,task_obj.cmd,task_obj.task_type,task_obj.user.id))
                res.append(p)
        #for r in res:
        #    print r.get()

        pool.close()
        pool.join()
    except ObjectDoesNotExist,e:
        sys.exit(e)

def by_ansible(task_id):
    pass


if __name__ == '__main__':
    required_args = ['-task_id','-run_type']    #必须参数

    for arg in required_args:
        if not arg in sys.argv:     #先判断是否输入了必须的参数
            sys.exit("arg [%s] is required" %arg)
    if len(sys.argv) < 5:   #脚本本身算1个参数，总共应至少输入5个参数
        sys.exit("5 arguments expected but %s given" %len(sys.argv))

    task_id = sys.argv[sys.argv.index("-task_id") + 1]  #找到-task_id后面跟的参数
    run_type = sys.argv[sys.argv.index("-run_type") + 1]

    if hasattr(__import__(__name__),run_type):  #判断模块是否有此方法（类是用self），如by_paramiko
        func = getattr(__import__(__name__),run_type)
        func(task_id)   #至少把task_id传给找到的方法，如by_paramiko
    else:
        sys.exit("Invalid run_type, only support [by_paramiko,by_ansible,by_saltstack]")