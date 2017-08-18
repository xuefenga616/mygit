#coding:utf-8
from NN_Class import NeuralNetwork
import numpy
from sklearn.datasets import load_digits                #数据集：阿拉伯数字
from sklearn.metrics import confusion_matrix, classification_report #对结果衡量
from sklearn.preprocessing import LabelBinarizer        #转化为二维数字类型
from sklearn.cross_validation import train_test_split   #交叉运算，数据集拆分

#根据8*8的灰度图上手写的数字，来预测0-9的数字
digits = load_digits()
X = digits.data
y = digits.target
X -= X.min()    #normalize the values to bring them into the range 0-1
X /= X.max()    #全转化到0、1之间

nn = NeuralNetwork([64,100,10],"logistic")              #64个维度特征，10个归类
X_train,X_test,y_train,y_test = train_test_split(X,y)   #拆分数据集
labels_train = LabelBinarizer().fit_transform(y_train)  #把0-9转化为二维数字类型，如[0 1 0 ..., 0 0 0]
labels_test = LabelBinarizer().fit_transform(y_test)
print("start fitting")
nn.fit(X_train,labels_train,epochs=3000)
predictions = []
for i in range(X_test.shape[0]):    #shape表示维度, shape[0]代表行
    o = nn.predict(X_test[i])
    predictions.append(numpy.argmax(o)) #argmax()得到最大概率的整数
print(confusion_matrix(y_test,predictions))         #准确率的表: 10*10的矩阵
print(classification_report(y_test,predictions))    #

