#coding:utf-8
from numpy import genfromtxt
from sklearn import datasets
from sklearn import linear_model

dataPath = "./Delivery.csv"
deliveryData = genfromtxt(dataPath, delimiter=",")  #csv文件根据逗号分隔符解析成矩阵
print("data")
print(deliveryData)

X = deliveryData[:, :-1]    #前面的：代表所有行，:-1代表最后1列之前
y = deliveryData[:, -1]

regr = linear_model.LinearRegression()  #线性回归分析
regr.fit(X,y)

print("coefficients:")
print(regr.coef_)           #多个斜率
print("intercept:")
print regr.intercept_       #截距

xPred = [102,6]
yPred = regr.predict(xPred)
print("predicted y: ",float(yPred))