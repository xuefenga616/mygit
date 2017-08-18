#coding:utf-8
import numpy
import random

#非线性回归
#梯度下降算法更新theta值，找到最低点
def gradientDescent(x,y,theta,alpha,m,numIterations):
    # alpha学习率  m总共多少实例  numIterations更迭次数
    xTrans = x.transpose()                  #转置矩阵
    for i in range(numIterations):          #更迭次数
        hypothesis = numpy.dot(x, theta)    #内积x * theta
        loss = hypothesis - y               #估计值与实际值的差值

        cost = numpy.sum(loss**2) / (2*m)   #类似方差
        print("Iteration %d | Cost: %f" %(i,cost))      #cost会逐渐减小

        gradient = numpy.dot(xTrans, loss) / m  #算出梯度下降算法中每次更新量

        theta = theta - alpha*gradient      #根据学习率、更新量，更新theta
    return theta

def genData(numPoints, bias, variance):     #多少行，偏差，方差（离散度衡量）
    x = numpy.zeros(shape=(numPoints,2))    #随机生成用0填充的2维矩阵
    y = numpy.zeros(shape=numPoints)

    for i in range(numPoints):
        # bias feature
        x[i][0] = 1
        x[i][1] = i
        #our target variable
        y[i] = (i+bias) + random.uniform(0,1)*variance
    return x,y

x,y = genData(100,25,10)
print("x:")
print(x)    # [1 0] ~ [1 99]
print("y:")
print(y)    #

m,n = numpy.shape(x)    # m代表多少行，n代表多少列

numIterations = 100000  #10000次循环
alpha = 0.0005          #学习率
theta = numpy.ones(n)   #初始化n维的theta
theta = gradientDescent(x,y,theta,alpha,m,numIterations)
print(theta)