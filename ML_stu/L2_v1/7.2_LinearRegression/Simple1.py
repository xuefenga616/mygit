#coding:utf-8
import numpy

def fitSLR(x, y):
    n = len(x)
    dinominator = 0     #分母
    numerator = 0       #分子
    for i in range(n):
        numerator += (x[i] - numpy.mean(x)) * (y[i] - numpy.mean(y))    #mean()是取平均值
        dinominator += (x[i] - numpy.mean(x))**2
    b1 = numerator / float(dinominator)         #斜率
    b0 = numpy.mean(y) / float(numpy.mean(x))   #截距
    return b0,b1

def predict(x, b0, b1):
    return b0 + x*b1

x = [1,3,2,1,3]
y = [14,24,18,17,27]

b0,b1 = fitSLR(x,y)
print("intercept: ", b0, "slope:", b1)
print(predict(4,b0,b1))