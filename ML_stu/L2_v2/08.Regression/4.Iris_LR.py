#coding:utf8
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = [u'simHei']
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib import patches

data = pd.read_csv("./iris.data", header=None)
data[4] = pd.Categorical(data[4]).codes     # 第四列分类0、1、2
X, y = np.split(data.values, (4,), axis=1)
# print(X)
# print(y)

# 仅使用前两列特征
X = X[:, :2]
lr = Pipeline([
    ("sc", StandardScaler()),                   # 目标值归一化处理
    ("poly", PolynomialFeatures(degree=2)),     # 特征从2项升维到2*2项
    ("clf", LogisticRegression())
])
lr.fit(X, y.ravel())
y_hat = lr.predict(X)
y_hat_prob = lr.predict_proba(X)
# print("y_hat = \n", y_hat)
# print("y_hat_prob = \n", y_hat_prob)
print(u"准确率: %.2f%%" %(100*np.mean(y_hat == y.ravel())))

# 画图
N, M = 500, 500     # 纵横各采样多少个值
X1_min, X1_max = X[:, 0].min(), X[:, 0].max()       # 4.3  7.9
X2_min, X2_max = X[:, 1].min(), X[:, 1].max()       # 2    4.4
print(X1_min, X1_max, X2_min, X2_max)
t1 = np.linspace(X1_min, X1_max, N)
t2 = np.linspace(X2_min, X2_max, M)
X1, X2 = np.meshgrid(t1, t2)    # 接受两个1维数组生成二维矩阵，500*2
X_test = np.stack((X1.flat, X2.flat), axis=1)       # 测试点
# print(X_test)

cm_light = matplotlib.colors.ListedColormap(['#77E0A0', '#FF8080', '#A0A0FF'])
cm_dark = matplotlib.colors.ListedColormap(['g', 'r', 'b'])
y_hat = lr.predict(X_test)
y_hat = y_hat.reshape(X1.shape) # 使之与输入的形状相同
plt.figure(facecolor="w")
plt.pcolormesh(X1, X2, y_hat, cmap=cm_light)
plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors="k", s=50, cmap=cm_dark)  # 样本的显示
plt.xlabel(u"花萼长度", fontsize=14)
plt.ylabel(u"花萼宽度", fontsize=14)
plt.xlim(X1_min, X1_max)
plt.ylim(X2_min, X2_max)
plt.grid()
patchs = [patches.Patch(color='#77E0A0', label='Iris-setosa'),
        patches.Patch(color='#FF8080', label='Iris-versicolor'),
        patches.Patch(color='#A0A0FF', label='Iris-virginica')]
plt.legend(hanlers=patches, fancybox=True, framealpha=0.8)
plt.title(u"鸢尾花Logistic回归分类效果 - 标准化", fontsize=17)
plt.show()