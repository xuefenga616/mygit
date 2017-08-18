#coding:utf8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
matplotlib.rcParams['font.sans-serif'] = [u'simHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# pandas读入
data = pd.read_csv("./Advertising.csv")
X = data[["TV", "Radio"]]
y = data["Sales"]
# print(X)
# print(y)

# 绘制1
plt.figure(facecolor="w")
plt.plot(data["TV"], y, "ro", label="TV")               # o是形状
plt.plot(data["Radio"], y, "g^", label="Radio")         # ^是形状
plt.plot(data["Newspaper"], y, "mv", label="Newspaper") #v是形状
plt.legend(loc="lower right")       # label右下角放置
plt.xlabel(u"广告花费", fontsize=16)
plt.ylabel(u"销售额", fontsize=16)
plt.title(u"广告花费与销售额对比数据", fontsize=20)
plt.grid()
# plt.show()

# 绘制2
plt.figure(figsize=(9,10), facecolor="w")
plt.subplot2grid((3,1), (0,0))
plt.plot(data["TV"], y, "ro")
plt.title("TV")
plt.grid()          # 加网格
plt.subplot2grid((3,1), (1,0))
plt.plot(data["Radio"], y, "g^")
plt.title("Radio")
plt.grid()
plt.subplot2grid((3,1), (2,0))
plt.plot(data["Newspaper"], y, "b*")
plt.title("Newspaper")
plt.grid()
plt.tight_layout()  # 自动布局

# plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
print(X_train.shape, y_train.shape)
linreg = LinearRegression()
model = linreg.fit(X_train, y_train)
print(model)
print(linreg.coef_, linreg.intercept_)

order = y_test.argsort(axis=0)      # 按列排序
y_test = y_test.values[order]
X_test = X_test.values[order, :]
y_hat = linreg.predict(X_test)
mse = np.average((y_hat - np.array(y_test)) ** 2)   # mean squared error
rmse = np.sqrt(mse)                                 # root mean squared error
print("MSE=", mse)
print("RMSE=", rmse)
print("R2=", linreg.score(X_train, y_train))
print("R2=", linreg.score(X_test, y_test))

plt.figure(facecolor="w")
t = np.arange(len(X_test))
plt.plot(t, y_test, "r-", linewidth=2, label=u"真实数据")
plt.plot(t, y_hat, "g-", linewidth=2, label=u"预测数据")
plt.legend(loc="upper right")
plt.title(u"线性回归预测销量", fontsize=18)
plt.grid()
plt.show()