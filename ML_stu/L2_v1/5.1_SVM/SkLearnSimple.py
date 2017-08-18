#coding:utf-8
from sklearn import svm

x = [[2,0],[1,1],[2,3]]
y = [0,0,1]     #实际归类
clf = svm.SVC(kernel="linear")
clf.fit(x,y)    #建立模型
print(clf)

#get support vectors 支持向量
print(clf.support_vectors_)

#get indices of support vectors 支持向量的索引
print(clf.support_)

#get number of support vectors for each class
print(clf.n_support_)   #各找到了1个支持向量
print(clf.predict([2,0]))   #预测