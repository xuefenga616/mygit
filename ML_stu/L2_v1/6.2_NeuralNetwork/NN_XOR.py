#coding:utf-8
from NN_Class import NeuralNetwork
import numpy

#用NN推断出异或结果
nn = NeuralNetwork([2,2,1], "tanh")         #输入层就两个神经元如：[0,0]
X = numpy.array([[0,0],[0,1],[1,0],[1,1]])  #列表转numpy
y = numpy.array([0,1,1,0])

nn.fit(X,y)
for i in [[0,0],[0,1],[1,0],[1,1]]:
    print(i, nn.predict(i))
