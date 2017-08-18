#coding:utf-8
from sklearn import svm
import numpy        #矩阵计算的库
import pylab        #画图的库

#创建40个点
numpy.random.seed(0)    #每次产生随机数的方法不变
X = numpy.r_[numpy.random.randn(20,2) - [2,2], numpy.random.randn(20,2) + [2,2]]    #在2,2(方差2)附近线性分布
Y = [0]*20 + [1]*20     #前20个点归类为0，后20个点归类为1
# print(X)

#fit the model
clf = svm.SVC(kernel="linear")
clf.fit(X,Y)

#得到超平面
#w_0 x + w_1 y + w_3 = 0    y = -(w_0 / w_1)x - (w_3 / w_1)
w = clf.coef_[0]        #取的w值，w是一个二维数组，有：w[0]、w[1]
a = -w[0] / w[1]        #直线斜率
xx = numpy.linspace(-5,5)   #从-5到5之间产生一些点作为x坐标
yy = a * xx - (clf.intercept_[0]) / w[1]    #clf.intercept_[0]即为w_3

#把相切的线画出来
b = clf.support_vectors_[0]     #找到第一个支持向量点
yy_down = a * xx + (b[1] - a * b[0])    #第一个点在底下，通过此点的直线，斜率与超平面斜率相同
b = clf.support_vectors_[-1]    #找到最后一个支持向量点
yy_up = a * xx + (b[1] - a * b[0])  #最后一个在右上面

print("w: ",w)
print("a: ",a)

print("support_vectors_: ",clf.support_vectors_)
print("clf_coef_: ",clf.coef_)

#开始画图
pylab.plot(xx, yy, 'k-')        #k-代表实线
pylab.plot(xx, yy_down, 'k--')  #k--代表虚线
pylab.plot(xx, yy_up, 'k--')

pylab.scatter(clf.support_vectors_[:,0],clf.support_vectors_[:,-1],s=80,facecolors='red')   #把支持向量点圈出来
pylab.scatter(X[:,0],X[:,1],c=Y,cmap=pylab.cm.Paired)   #X[:,0]代表左下的点, X[:,1]代表右上的点 Y = [0]*20 + [1]*20

pylab.axis("tight")
pylab.show()