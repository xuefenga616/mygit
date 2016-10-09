#_*_coding:utf-8_*_

import templates

g1 = templates.LinuxTemplate()
g1.group_name  = 'Test groups'
g1.hosts = ['192.168.1.12','192.168.1.13']

#--------

g2 = templates.NetworkTemplate()
g2.group_name = 'puppet server groups'
g2.hosts = ['192.168.1.12','10.0.10.3']


monitored_groups= [g1,g2]

