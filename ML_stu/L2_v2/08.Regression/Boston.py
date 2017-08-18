#coding:utf-8
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

def not_empty(s):
    return s != ""

file_data = pd.read_csv("./housing.data", header=None)
data = np.empty((len(file_data), 14))       # empty创建的数组中，包含的元素均为无意义的数值
for i,d in enumerate(file_data.values):
    # d = filter(not_empty, d[0].split(" "))
    d = [float(j) for j in d[0].split(" ") if j != ""]
    data[i] = d
# print(data)
X, y = np.split(data, (13,), axis=1)
print(u"样本个数：%d，特征个数：%d" %X.shape)
print(y.shape)
y = y.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
model = Pipeline([
    ("ss", StandardScaler()),
    ("poly", PolynomialFeatures(degree=3, include_bias=True)),
    ("linear", ElasticNetCV(l1_ratio=[0.1,0.3,0.5,0.7,0.99,1], alphas=np.logspace(-3,2,5),
                            fit_intercept=False, max_iter=1e3, cv=3))
])
model.fit(X_train, y_train)
linear = model.get_params("linear")["linear"]
print(u"超参数:", linear.alpha_)
print(u"L1 ratio:", linear.l1_ratio_)

order = y_test.argsort(axis=0)
y_test = y_test[order]
X_test = X_test[order, :]
y_pred = model.predict(X_test)
r2 = model.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
print("R2", r2)
print(u"均方误差:", mse)

t = np.arange(len(y_pred))
plt.figure(facecolor="w")
plt.plot(t, y_test, "r-", lw=2, label=u"真实值")
plt.plot(t, y_pred, "g-", lw=2, label=u"估计值")
plt.legend(loc="best")
plt.title(u"波士顿房价预测", fontsize=18)
plt.xlabel(u"样本编号", fontsize=15)
plt.ylabel(u"房屋价格", fontsize=15)
plt.grid()
plt.show()