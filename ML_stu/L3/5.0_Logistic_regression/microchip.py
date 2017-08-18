#coding:utf-8
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures

def loadData(file, delimeter):
    data = np.loadtxt(file, delimiter=delimeter)    # delimeter是分隔符
    print("Dimensions: ", data.shape)

    return data

def plotData(data, label_x, label_y, label_neg, label_pos, axes=None):
    neg = data[:, 2] == 0       # 负样本下标
    pos = data[:, 2] == 1       # 正样本下标

    if axes is None:
        axes = pyplot.gca()           # 获取当前的坐标
    # marker样式 c颜色 s大小
    axes.scatter(data[pos][:, 0], data[pos][:, 1], marker="+", c="k", s=60, linewidth=2, label=label_pos)
    axes.scatter(data[neg][:, 0], data[neg][:, 1], c="y", s=60, label=label_neg)
    axes.set_xlabel(label_x)
    axes.set_ylabel(label_y)
    axes.legend(frameon=True, fancybox=True)
    # pyplot.show()

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def lossFunctionReg(theta, reg, *args):
    m = y.size
    h = sigmoid(XX.dot(theta))      # h初始化成0.5

    # 加上l2正则化项，θ0不需要正则化
    J = (-1 / m) * (np.log(h).T.dot(y) + np.log(1-h).T.dot(1-y)) + (reg / (2*m)) * np.sum(np.square(theta[1:]))
    # print(np.sum(np.square(theta[1:])))

    if np.isnan(J[0]):
        return np.inf
    return J[0]

# 求解梯度
def gradientReg(theta, reg, *args):
    m = y.size
    h = sigmoid(XX.dot(theta.reshape(-1, 1)))

    grad = (1 / m) * XX.T.dot(h-y) + (reg / m) * np.r_[[[0]], theta[1:].reshape(-1,1)]

    return grad.flatten()   # 矩阵合并成列表

def predict(theta, X, threshold=0.5):
    p = sigmoid(X.dot(theta.T)) >= threshold
    return p.astype("int")

data2 = loadData("./data2.txt", ",")
X = np.c_[np.ones((data2.shape[0],1)), data2[:, :2]]  # 列向插入1列全是1的数
y = np.c_[data2[:, 2]]
# print(X,y)
# plotData(data2, "Microchip Test 1", "Microchip Test 2", "y = 0", "y = 1")

poly = PolynomialFeatures(6)    # 做特征映射，生成多项式特征，最高次数为6
XX = poly.fit_transform(data2[:, :2])
print(XX.shape)

initial_theta = np.zeros(XX.shape[1])
# print(np.r_[[[0]], initial_theta[1:].reshape(-1,1)])    # numpy.r_ 沿着一个方向组合，第一行前插入一行加个0

# print(lossFunctionReg(initial_theta, 1, XX, y))
# print(gradientReg(initial_theta, 1, XX, y))

# fig, axes = pyplot.subplots(1, 3, sharey=True, figsize=(17,5))
for i, C in enumerate([0, 1, 100]):     #i,C 遍历下标及数值
    pass
res2 = minimize(lossFunctionReg, initial_theta, args=(1, XX, y), method=None, jac=gradientReg, options={"maxiter":3000, "disp":True})
# 准确率
accuracy = 100 * sum(predict(res2.x, XX)==y.ravel()) / y.size
# print(accuracy)
plotData(data2, "Microchip Test 1", "Microchip Test 2", "y = 0", "y = 1")
# 画出决策边界
x1_min, x1_max = X[:, 1].min(), X[:, 1].max()
x2_min, x2_max = X[:, 2].min(), X[:, 2].max()
xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max), np.linspace(x2_min, x2_max))
h = sigmoid(poly.fit_transform(np.c_[xx1.ravel(), xx2.ravel()]).dot(res2.x))
h = h.reshape(xx1.shape)
pyplot.contour(xx1, xx2, h, [0.5], linewidths=1, colors='g')
# pyplot.set_title("Train accuracy {}% with Lambda = {}".format(np.round(accuracy,decimals=2), C))

pyplot.show()
