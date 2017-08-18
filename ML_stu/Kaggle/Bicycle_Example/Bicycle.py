#coding:utf-8
import numpy as np
import pandas as pd
from matplotlib import pyplot
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import cross_validation
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.learning_curve import learning_curve
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import explained_variance_score

# jupyter notebook
def feature_preprocess(data):
    data["month"] = pd.DatetimeIndex(data.datetime).month
    data["dayofweek"] = pd.DatetimeIndex(data.datetime).dayofweek
    data["day"] = pd.DatetimeIndex(data.datetime).day
    data["hour"] = pd.DatetimeIndex(data.datetime).hour
    data["dateDays"] = (data.day - data.day[0]).astype("int64")  # 产出一个时间长度（猜测越往后骑车的越多）
    # print(date.head())

    # 周末既然有不同，就单独拿2列出来分别给周六、日
    data["Saturday"] = 0
    data["Sunday"] = 0
    data.Saturday[data.dayofweek == 5] = 1
    data.Sunday[data.dayofweek == 6] = 1

    # 统计注册/非注册用户租赁情况
    byday = data.groupby("dayofweek")
    # print(byday["casual"].sum().reset_index())
    # print(byday["registered"].sum().reset_index())

    fig, axs = pyplot.subplots(3, 4, sharey=True)
    data.plot(kind="scatter", x="temp", y="count", ax=axs[0,0], figsize=(16,8))
    data.plot(kind="scatter", x="atemp", y="count", ax=axs[0,1])
    data.plot(kind="scatter", x="humidity", y="count", ax=axs[0,2])
    data.plot(kind="scatter", x="windspeed", y="count", ax=axs[0,3])
    data.plot(kind="scatter", x="month", y="count", ax=axs[1,0])
    data.plot(kind="scatter", x="hour", y="count", ax=axs[1,1])

    pyplot.subplot2grid((3,4),(2,0))
    data.groupby("dayofweek")["casual"].sum().plot(kind="bar")
    pyplot.ylabel("count")
    pyplot.xlabel(u"未注册用户 dayofweek")

    pyplot.subplot2grid((3, 4), (2, 1))
    data.groupby("dayofweek")["registered"].sum().plot(kind="bar")
    pyplot.xlabel(u"注册用户 dayofweek")

    # pyplot.show()

    dateRel = data.drop(["datetime", "dayofweek", "day", "casual", "registered"], axis=1)
    # print(dateRel.head())
    # print(dateRel.dtypes)

    # 把连续值得属性放入1个dict中
    featureConCols = ["temp", "atemp", "humidity", "windspeed", "dateDays", "month", "hour"]
    dataFeatureCon = dateRel[featureConCols]
    # dataFeatureCon = dataFeatureCon.fillna("NA")
    X_dictCon = dataFeatureCon.T.to_dict().values()

    # 把离散值得属性放到另一个dict中
    featureCatCols = ["season", "holiday", "workingday", "weather", "Saturday", "Sunday"]
    dataFeatureCat = dateRel[featureCatCols]
    # dataFeatureCat = dataFeatureCat.fillna("NA")
    X_dictCat = dataFeatureCat.T.to_dict().values()

    # 向量化特征
    vec = DictVectorizer(sparse=False)
    X_vec_cat = vec.fit_transform(X_dictCat)
    X_vec_con = vec.fit_transform(X_dictCon)

    # 标准化连续值数据，使均值为0，方差为1
    scaler = preprocessing.StandardScaler().fit(X_vec_con)
    X_vec_con = scaler.transform(X_vec_con)
    # print(X_vec_con)
    # one-hot编码
    enc = preprocessing.OneHotEncoder()
    enc.fit(X_vec_cat)
    X_vec_cat = enc.transform(X_vec_cat).toarray()
    # print(X_vec_cat)

    # 把离散和连续的特征都组合在一起
    X_vec = np.concatenate((X_vec_con, X_vec_cat), axis=1)
    # print(X_vec)

    y_vec = data["count"].values.astype(float)

    return X_vec, y_vec

def paramSearch(X_vec, y_vec):
    X_train,X_test,y_train,y_test = cross_validation.train_test_split(X_vec, y_vec, test_size=0.2, random_state=0)

    tuned_params = [{"n_estimators": [10,100,500]}]
    scores = ["r2"]
    for score in scores:
        clf = GridSearchCV(RandomForestRegressor(), tuned_params, cv=5, scoring=score)
        clf.fit(X_train, y_train)
        print(clf.best_estimator_)
        for params,mean_score,scores in clf.grid_scores_:
            print("%.3f (+/-%.3f) for %r" %(mean_score, scores.std()*2, params))

    # tuned_params = [{"C": [10, 100, 1000], "gamma": [1e-3, 1e-4]}]
    # scores = ["precision", "recall"]
    # for score in scores:
    #     clf = GridSearchCV(svm.SVC(), tuned_params, cv=5, scoring="%s_weighted" %score)
    #     clf.fit(X_train, y_train)
    #     print(clf.best_estimator_)
    #     for params,mean_score,scores in clf.grid_scores_:
    #         print("%.3f (+/-%.3f) for %r" %(mean_score, scores.std()*2, params))

def fit(X_vec, y_vec):
    # 切分数据集
    cv = cross_validation.ShuffleSplit(len(X_vec), n_iter=3, test_size=0.2, random_state=0)

    # 岭回归
    # for train,test in cv:
    #     svc = linear_model.Ridge().fit(X_vec[train], y_vec[train])
    #     print("train score: %.3f, test score: %.3f\n" %(
    #         svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
    #     ))

    # 支持向量机，C是正则化项因子，gamma是核函数gamma因子
    # for train,test in cv:
    #     # SVR既可以解决分类问题，又可以解决回归问题
    #     svc = svm.SVR(kernel="rbf", C=10, gamma=1e-3).fit(X_vec[train], y_vec[train])
    #     print("train score: %.3f, test score: %.3f\n" % (
    #         svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
    #     ))

    # 随机森林回归
    for train,test in cv:
        svc = RandomForestRegressor(n_estimators=100, max_depth=10).fit(X_vec[train], y_vec[train])
        print("train score: %.3f, test score: %.3f\n" % (
            svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
        ))

def plotCurve(estimator, X, y, ylim=None, cv=None):
    # title = "Learning Curves (Random Forest, n_estimators = 100)"
    # pyplot.figure()     # 创建1副图
    pyplot.subplot2grid((3, 4), (1, 2), rowspan=2, colspan=2)
    # pyplot.title(title)
    if ylim is not None:
        pyplot.ylim(*ylim)
    pyplot.xlabel("Learning Curves (Random Forest, n_estimators = 100)", fontsize=13)
    pyplot.ylabel("Score")

    train_size, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=16, train_sizes=np.linspace(0.1,1.0,5)
    )   #numpy.linspace()设置曲线刻度
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    pyplot.grid()       # 显示网格
    pyplot.fill_between(train_size, train_scores_mean - train_scores_std,
                        train_scores_mean + train_scores_std, alpha=0.2, color="r")
    pyplot.fill_between(train_size, test_scores_mean - test_scores_std,
                        test_scores_mean + test_scores_std, alpha=0.2, color="g")
    pyplot.plot(train_size, train_scores_mean, "o-", color="r", label="Training score")
    pyplot.plot(train_size, test_scores_mean, "o-", color="g", label="Cross-validation score")
    pyplot.legend(loc="best")

    pyplot.show()

if __name__ == "__main__":
    df_train = pd.read_csv("./kaggle_bike_competition_train.csv", header=0)
    # print(df_train.head())

    X_vec, y_vec = feature_preprocess(df_train)

    # paramSearch(X_vec, y_vec)
    fit(X_vec, y_vec)

    cv = cross_validation.ShuffleSplit(X_vec.shape[0], n_iter=10, test_size=0.2, random_state=0)
    estimator = RandomForestRegressor(n_estimators=100, max_depth=10)
    plotCurve(estimator, X_vec, y_vec, (0.0,1.01), cv=cv)   #ylim设置y轴范围

