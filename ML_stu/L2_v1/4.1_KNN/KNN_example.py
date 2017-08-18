#coding:utf-8
from sklearn import neighbors   #KNN
from sklearn import datasets    #数据集

knn = neighbors.KNeighborsClassifier()  #分类器

iris = datasets.load_iris()     #加载数据集: 花：虹膜iris：（萼片长、萼片宽、花瓣长、花瓣宽）
print(iris)

knn.fit(iris.data, iris.target)     #建立模型，分别传入特征值和结果
predictedLabel = knn.predict([[6.5,3.1,5.1,2]]) #预测花属于哪一种
print(predictedLabel)