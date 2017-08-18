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

def lossfunction(theta, X, y):
    m = y.size
    h = sigmoid(X.dot(theta))

    J = (-1 / m) * (np.log(h).T.dot(y) + np.log(1-h).T.dot(1-y))
    # print(J)

    if np.isnan(J[0]):      # 非常小的数
        return np.inf       # 转换为0
    return J[0]

# 求解梯度
def gradient(theta, X, y):
    m = y.size
    h = sigmoid(X.dot(theta.reshape(-1, 1)))
    # print(h, y)   # h都是0.5

    grad = (1 / m) * X.T.dot(h - y)     # X的转置是3行100列，y是100行1列，乘积是3行1列

    return grad.flatten()

def predict(theta, X, threshold=0.5):
    p = sigmoid(X.dot(theta.T)) >= threshold
    return p.astype("int")

data = loadData("./data1.txt", ",")
X = np.c_[np.ones((data.shape[0],1)), data[:, :2]]  # 列向插入1列全是1的数
y = np.c_[data[:, 2]]
# print(y)

# plotData(data, "Exam 1 score", "Exam 2 score", "Not admitted", "Admitted")

initial_thetha = np.zeros(X.shape[1])   # 初始一个矩阵[0, 0, 0]
cost = lossfunction(initial_thetha, X, y)
print("Cost:\n", cost)
# print(X.dot(initial_thetha.reshape(-1, 1)))
grad = gradient(initial_thetha, X, y)
print("Grad:\n", grad)

# 最小化损失函数
res = minimize(lossfunction, initial_thetha, args=(X,y), method=None, jac=gradient, options={"maxiter":400, "disp":True})
# print(res)

# print(sigmoid(np.array([1, 45, 85]).dot(res.x.T)))
p = predict(res.x, X)
print("Train accuracy {}%".format(100*sum(p == y.ravel())/p.size))

# pyplot.scatter(45, 85, s=60, c="r", marker="v", label="(45, 85)")
plotData(data, "Exam 1 score", "Exam 2 score", "Failed", "Pass")
x1_min, x1_max = X[:, 1].min(), X[:, 1].max()
x2_min, x2_max = X[:, 2].min(), X[:, 2].max()
xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max), np.linspace(x2_min, x2_max))
h = sigmoid(np.c_[np.ones((xx1.ravel().shape[0], 1)), xx1.ravel(), xx2.ravel()].dot(res.x))
h = h.reshape(xx1.shape)
pyplot.contour(xx1, xx2, h, [0.5], linewidths=1, colors='b')
pyplot.scatter(45, 85, s=60, c="r", marker="v", label="(45, 85)")
pyplot.show()