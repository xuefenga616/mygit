#_*_coding:utf-8_*_

import generic
from data_process import avg,hit,last 
class cpu(generic.BaseService):
    def __init__(self):
        super(cpu,self).__init__()
        self.name = 'linux_cpu'
        self.interval = 30
        self.plugin_name = 'get_cpu_status'
        self.triggers = {
                'idle':{'func':avg,
                        'minutes': 1,
                        'operator': 'lt',
                        'warning':20,
                        'critical':5,
                        'data_type': 'percentage'
                        },
                'iowait':{'func':avg,
                        'minutes': 1,
                        'operator': 'gt',
                        'threshold': 3,  #阈值，hit3次
                        'warning':50,
                        'critical':80,
                        'data_type': 'percentage'
                        },
                         }
        
class memory(generic.BaseService):
    def __init__(self):
        super(memory,self).__init__()
        self.name = 'linux_memory'
        self.interval = 30
        self.plugin_name = 'get_memory_info'
        self.triggers = {
                'MemUsage':{'func':avg,
                        'minutes': 1,
                        'operator': 'gt',
                        'warning':80,
                        'critical':90,
                        'data_type': 'percentage'
                        }
                         }

class load(generic.BaseService):
    def __init__(self):
        super(load,self).__init__()
        self.name = 'linux_load'
        self.interval = 20
        self.plugin_name = 'get_load_info'
        self.triggers = {
                'load1':{'func':avg,
                        'minutes': 1,
                        'operator': 'gt',
                        'warning':70,
                        'critical':80,
                        'data_type': 'percentage'
                        }
                         }

        


if __name__ == '__main__':
    c = cpu()
    print c.name ,c.interval,c.plugin_name
