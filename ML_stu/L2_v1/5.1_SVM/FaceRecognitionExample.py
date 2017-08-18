#coding:utf-8
from time import time
import logging
import matplotlib.pyplot as plt     # 最后绘图

from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import  confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# 数据集下载
lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

#返回数据集实例个数、高、宽
n_samples, h, w = lfw_people.images.shape

#提取特征向量的矩阵
X = lfw_people.data
n_features = X.shape[1]     #向量的维度是多少，0代表行数，1代表列数

#每个实例对应是哪个人脸
y = lfw_people.target
target_names = lfw_people.target_names
n_classes = target_names.shape[0]   #多少个人，0代表行数

print("n_sample: %d" % n_samples)
print("n_feature %d" % n_features)
print("n_classes %d" % n_classes)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25)     #拆分成训练集和测试集

n_components = 150      #150个元素

print("extracting the top %d eigenfaces from the %d faces" % (n_components,X_train.shape[0]))
# 把高维的特征向量降维
t0 = time()
pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
print("done in %0.3fs" %(time()-t0))

#人脸照片上提取特征值
eigenfaces = pca.components_.reshape((n_components,h,w))
print("projecting the input data on the eigenfaces orthonomal basis")

t0 = time()
X_train_pca = pca.transform(X_train)    #降维
X_test_pca = pca.transform(X_test)
print("done in %0.3fs" %(time()-t0))

#根据降维后的特征向量，选择合适的核函数
print("fitting the classfier to the training set ")
t0 = time()
parag_grid ={'C':[1e3,5e3,1e4,5e4,1e5],'gamma':[0.0001,0.0005,0.001,0.005,0.01,0.1],}
clf = GridSearchCV(SVC(kernel='rbf',class_weight='auto'),parag_grid)
clf = clf.fit(X_train_pca,y_train)      #
print("done in %0.3fs" %(time()-t0))
print("best estimator found by grid search:")
print(clf.best_estimator_)

#测试
print("predict the people's namne on the test set")
t0=time()
y_pred = clf.predict(X_test_pca)
print("done in %0.3fs " %(time()-t0))
print(classification_report(y_test,y_pred,target_names=target_names))
print(confusion_matrix(y_test,y_pred,labels=range(n_classes)))

#画图
def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks()
        plt.yticks()


def title(y_pred, y_test, target_names, i):
    pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
    return 'predicted :%s \ntrue:  %s' % (pred_name, true_name)


prediction_titles = [title(y_pred, y_test, target_names, i)
                     for i in range(y_pred.shape[0])]

plot_gallery(X_test, prediction_titles, h, w)
eigenface_title = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
plot_gallery(eigenfaces, eigenface_title, h, w)

plt.show()