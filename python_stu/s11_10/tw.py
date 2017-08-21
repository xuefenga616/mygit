#coding:utf-8
__author__ = 'Administrator'
from twisted.internet import protocol
from twisted.internet import reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

factory = protocol.ServerFactory()
factory.protocol = Echo

reactor.listenTCP(8080,factory)
reactor.run()