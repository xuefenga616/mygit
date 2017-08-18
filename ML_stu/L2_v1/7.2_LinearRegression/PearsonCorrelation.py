#coding:utf-8
import numpy
import math

def computeCorrelation(X,Y):    # R : 相关度
    xBar = numpy.mean(X)    # 平均值
    yBar = numpy.mean(Y)
    SSR = 0
    varX = 0
    varY = 0
    for i in range(len(X)):
        diffXXBar = X[i] - xBar
        diffYYBar = Y[i] - yBar
        SSR += (diffXXBar * diffYYBar)
        varX += diffXXBar**2
        varY += diffYYBar**2

    SST = math.sqrt(varX * varY)
    return SSR / SST


def polyfit(x,y,degree):    # r^2 : 决定系数
    results = {}

    coeffs = numpy.polyfit(x,y,degree)  # 算出斜率、截距、几次线性回归
    results['polynomial'] = coeffs.tolist()
    # print(results['polynomial'])

    # r-squared
    p = numpy.poly1d(coeffs)    # 直线的方程
    # fit values, and mean
    yhat = p(x)                 # 估计值
    ybar = numpy.sum(y)/len(y)  # 实际值的平均值
    ssreg = numpy.sum((yhat-ybar)**2)
    sstot = numpy.sum((y - ybar)**2)
    results['determination'] = ssreg / sstot    #决定系数
    return results

testX = [1,3,8,7,9]
testY = [10,12,24,21,34]

print(computeCorrelation(testX,testY))
print(computeCorrelation(testX,testY)**2)
print(polyfit(testX,testY,1)['determination'])