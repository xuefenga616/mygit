#coding:utf-8
import numpy as np
from numpy import *

def sigmoid(X):     #求倒数
    return 1.0 / (1 + exp(-X))

class Network(object):
    def __init__(self,sizes):   # [2,3,1]有几层，每层有几个神经元
        self.num_layeres = len(sizes)   #层数
        self.sizes = sizes
        # np.random.rand(y,1) 随机从正态分布（均值0，方差1）中生成
        self.biases = [np.random.randn(y,1) for y in sizes[1:]] #偏向 y行1列
        # print self.biases
        self.weights = [np.random.randn(y,x) for x,y in zip(sizes[:-1],sizes[1:])]  #y行x列 zip是结合两个集合
        # print self.weights

    def feedforward(self,a):    # a代表输入的元素，b代表偏向，w代表权重
        # w*a + b
        for b,w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w,a) + b)
        return a

    # 随机梯度下降算法
    def SGD(self,training_data,epochs,mini_batch_size,eta,test_data=None):  # eta代表学习率
        if test_data is not None:
            n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)   # 把训练集里的元素，随机打乱
            # 一次取len(training_data)/mini_batch_size个值，不连续
            mini_batches = [training_data[k:k+mini_batch_size] for k in xrange(0,n,mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print "Epoch %s: %s / %s" %(j, self.evaluate(test_data), n_test)
            else:
                print "Epoch %s complete" %j

    # 更新权重weight和偏向bias
    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x,y)
            nabla_b = [nb+dnb for nb,dnb in zip(nabla_b,delta_nabla_b)]
            nabla_w = [nw+dnw for nw,dnw in zip(nabla_w,delta_nabla_w)]
        self.weights = [w - eta*nw/len(mini_batch) for w,nw in zip(self.weights,nabla_w)]
        self.biases = [b - eta*nb/len(mini_batch) for b,nb in zip(self.biases,nabla_b)]

    def backprop(self, x, y):
        pass

    def evaluate(self, test_data):
        pass



net = Network([2,3,1])