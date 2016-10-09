#_*_coding:utf-8_*_

import generic
from data_process import avg,hit,last 
class nic(generic.BaseService):
    def __init__(self):
        super(nic,self).__init__()
        self.name = 'nic_network'
        self.interval = 120
        self.plugin_name = 'get_network_info'
        self.triggers = {
                'in':{'func':avg,
                        'minutes': 15,
                        'operator': 'lt',
                        'warning':20,
                        'critical':5,
                        'data_type': 'percentage'
                        },
                         }
        



if __name__ == '__main__':
    pass
