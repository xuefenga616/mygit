#coding:utf8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
matplotlib.rcParams['font.sans-serif'] = [u'simHei']
matplotlib.rcParams['axes.unicode_minus'] = False

data = pd.read_csv("./Advertising.csv")
X = data[["TV", "Radio", "Newspaper"]]
y = data["Sales"]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
alpha_can = np.logspace(-3, 2, 10)      # 从1e-3到1e2
ridge_model = GridSearchCV(Ridge(), param_grid={"alpha": alpha_can}, cv=5)  # Ridge()岭回归
ridge_model.fit(X_train, y_train)
print(u"超参数: \n", ridge_model.best_params_)

order = y_test.argsort(axis=0)
y_test = y_test.values[order]
X_test = X_test.values[order, :]
y_hat = ridge_model.predict(X_test)
print(ridge_model.score(X_test, y_test))
mse = np.average((y_hat - np.array(y_test)) ** 2)   # mean squared error
rmse = np.sqrt(mse)
print(mse, rmse)

t = np.arange(len(X_test))
plt.figure(facecolor="w")
plt.plot(t, y_test, "r-", linewidth=2, label=u"真实数据")
plt.plot(t, y_hat, "g-", linewidth=2, label=u"预测数据")
plt.title(u"线性回归预测销量", fontsize=18)
plt.legend(loc="lower right")
plt.grid()
plt.show()