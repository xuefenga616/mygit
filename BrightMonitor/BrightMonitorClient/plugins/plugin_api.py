#_*_coding:utf-8_*_
__author__ = 'xuefeng'

from linux import sysinfo,load,cpu,memory,network,host_alive



def LinuxSysInfo():
    return  sysinfo.collect()

def get_linux_cpu():
    return cpu.monitor()

def host_alive_check():
    return host_alive.monitor()

def GetNetworkStatus():
    return network.monitor()

def get_memory_info():
    return memory.monitor()

def get_load_info():
    return load.monitor()