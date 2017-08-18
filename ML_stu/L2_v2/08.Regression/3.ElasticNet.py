#coding:utf8
import numpy as np
from sklearn.linear_model import LinearRegression,RidgeCV,LassoCV,ElasticNetCV
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
import matplotlib
matplotlib.rcParams['font.sans-serif'] = [u'simHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import warnings
from sklearn.exceptions import ConvergenceWarning

def xss(y, y_hat):
    y = y.ravel()       # 多维数组降为一维
    y_hat = y_hat.ravel()

    tss = ((y - np.average(y))**2).sum()
    rss = ((y_hat - y)**2).sum()
    ess = ((y_hat - np.average(y))**2).sum()
    r2 = 1 - rss/tss

    tss_list.append(tss)
    rss_list.append(rss)
    ess_list.append(ess)
    ess_rss_list.append(rss + ess)

    corr_coef = np.corrcoef(y, y_hat)[0, 1]
    return r2, corr_coef

if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
    np.random.seed(0)
    # np.set_printoptions(linewidth=1000)
    N = 9
    X = np.linspace(0, 6, N) + np.random.randn(N)   # 0-6随机9个数
    X = np.sort(X)
    y = X**2 - 4*X - 3 + np.random.randn(N)
    X.shape = -1, 1
    y.shape = -1, 1

    models = [      # pipeline的目的就是当设置不同的参数时组合几个可以一起交叉验证的步骤
        Pipeline([
            ("poly", PolynomialFeatures()),
            ("linear", LinearRegression(fit_intercept=False))   # fit_intercept表示是否计算截距
        ]),
        Pipeline([
            ("poly", PolynomialFeatures()),
            ("linear", RidgeCV(alphas=np.logspace(-3,2,50), fit_intercept=False))
        ]),
        Pipeline([
            ("poly", PolynomialFeatures()),
            ("linear", LassoCV(alphas=np.logspace(-3, 2, 50), fit_intercept=False))
        ]),
        Pipeline([
            ("poly", PolynomialFeatures()),
            ("linear", ElasticNetCV(alphas=np.logspace(-3,2,50), l1_ratio=[.1,.5,.7,.9,.95,.99,1],
                                    fit_intercept=False))
        ])
    ]

    plt.figure(figsize=(18,12), facecolor="w")
    d_pool = np.arange(1, N, 1)
    m = d_pool.size
    clrs = []       # 颜色
    for c in np.linspace(16711680, 255, m):
        clrs.append("#%06x" %int(c))     # %x表示16进制输出

    line_width = np.linspace(5, 2, m)
    titles = u"线性回归", u"Ridge回归", u"LASSO", u"ElaticNet"
    tss_list = []
    rss_list = []
    ess_list = []
    ess_rss_list = []
    for t in range(4):
        model = models[t]
        plt.subplot(2, 2, t+1)
        plt.plot(X, y, "ro", ms=10, zorder=N)

        for i,d in enumerate(d_pool):
            model.set_params(poly__degree=d)
            model.fit(X, y.ravel())
            lin = model.get_params("linear")["linear"]
            output = u"%s: %d阶，系数为：" %(titles[t], d)
            if hasattr(lin, "alpha_"):
                idx = output.find(u"系数")
                output = output[:idx] + ("alpha=%.6f," %lin.alpha_) + output[idx:]
            if hasattr(lin, "l1_ratio_"):   # 根据交叉验证结果，从输入l1_ratio(list)中选择的最优l1_ratio_(float)
                idx = output.find(u"系数")
                output = output[:idx] + ("l1_ratio=%.6f," %lin.l1_ratio_) + output[idx:]
            print(output, lin.coef_.ravel())
            X_hat = np.linspace(X.min(), X.max(), num=100)
            X_hat.shape = -1, 1
            y_hat = model.predict(X_hat)
            s = model.score(X, y)
            r2, corr_coef = xss(y, model.predict(X))

            z = N - 1 if d == 2 else 0
            label = u"%d阶, $R^2$=%.3f" %(d,s)
            if hasattr(lin, "l1_ratio_"):
                label += ", L1 ratio=%.2f" %lin.l1_ratio_
            plt.plot(X_hat, y_hat, color=clrs[i], lw=line_width[i], alpha=0.75, label=label, zorder=z)
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.title(titles[t], fontsize=18)
        plt.xlabel("X", fontsize=16)
        plt.ylabel("Y", fontsize=16)
    plt.tight_layout(1, rect=(0,0,1,0.95))
    plt.suptitle(u"多项式曲线拟合比较", fontsize=22)
    # plt.show()

    y_max = max(max(tss_list), max(ess_rss_list)) * 1.05
    plt.figure(figsize=(9,7), facecolor="w")
    t = np.arange(len(tss_list))
    plt.plot(t, tss_list, "ro-", lw=2, label="TSS(Total Sum of Squares)")
    plt.plot(t, ess_list, "mo-", lw=1, label="ESS(Explained Sum of Squares)")
    plt.plot(t, tss_list, "bo-", lw=1, label="RSS(Residual Sum of Squares)")
    plt.plot(t, tss_list, "go-", lw=2, label="ESS+RSS")
    plt.ylim((0, y_max))
    plt.legend(loc="center right")
    plt.xlabel(u"实验：线性回归/Ridge/LASSO/Elastic Net", fontsize=15)
    plt.ylabel(u"XSS值", fontsize=15)
    plt.title(u"总平方和TSS=?", fontsize=18)
    plt.grid()
    plt.show()