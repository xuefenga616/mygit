#_*_coding:utf-8_*_

from services import linux,network

class BaseTemplate(object):
    def __init__(self):
        self.name = 'YourTemplateName'
        self.group_name = 'YourGroupName'
        self.hosts = []
        self.services = []

class LinuxTemplate(BaseTemplate):
    def __init__(self):
        super(LinuxTemplate, self).__init__()
        self.name = 'LinuxTemplate'
        self.services= [
                linux.cpu,
                linux.memory,       
                linux.load,
                        ]

class NetworkTemplate(BaseTemplate):
    def __init__(self):
        super(NetworkTemplate, self).__init__()
        self.name = 'NetworkTemplate'
        self.services= [
                network.nic
                        ]

if __name__ == "__main__":
    t = LinuxTemplate()
    t.hosts = ['192.168.1.12','192.168.1.13']

    for service in t.services:
        service = service()
        if service.name == 'linux_cpu':
            service.interval = 50
        print service.name, service.interval

    print "-------t2 below-------"
    t2 = LinuxTemplate()
    t.hosts = ['10.0.10.2','10.0.10.3']

    for service in t.services:
        service = service()
        print service.name, service.interval

