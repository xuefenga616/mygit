#coding:utf-8
import math

import numpy as np
import pandas as pd

from sklearn.cross_validation import KFold
from sklearn.linear_model import SGDClassifier
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier
from matplotlib import pyplot
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sklearn.learning_curve import learning_curve
import json

def train():
    trainDf = pd.read_csv("data_train.csv")
    X_frame = pd.DataFrame(
        trainDf, index=None,
        columns=["invited", "user_reco", "evt_p_reco", "user_pop", "frnd_inf1", "evt_pop"]
    )
    X = np.matrix(X_frame)
    y = np.array(trainDf.interested)
    clf = SGDClassifier(loss="log", penalty="l2")
    clf.fit(X, y)
    return clf

def validate():
    # 10折的交叉验证
    trainDf = pd.read_csv("data_train.csv")
    X = np.matrix(pd.DataFrame(trainDf, index=None,
                               columns=["invited", "user_reco", "evt_p_reco",
                                        "user_pop", "frnd_inf1", "evt_pop"]))
    y = np.array(trainDf.interested)
    nrows = len(trainDf)
    kfold = KFold(nrows, 10)
    avgAccuracy = 0
    run = 0
    for train, test in kfold:
        Xtrain, Xtest, ytrain, ytest = X[train], X[test], y[train], y[test]
        clf = SGDClassifier(loss="log", penalty="l2")
        clf.fit(Xtrain, ytrain)
        accuracy = 0
        ntest = len(ytest)
        for i in range(0, ntest):
            yt = clf.predict(Xtest[i, :])
            if yt == ytest[i]:
                accuracy += 1
        accuracy = accuracy / ntest
        print("accuracy (run %d): %f" % (run, accuracy))
        avgAccuracy += accuracy
        run += 1
    print("Average accuracy", (avgAccuracy / run))

def fit_test():
    data = pd.read_csv("data_train.csv")
    X_frame = pd.DataFrame(
        data, index=None,
        columns=["invited", "user_reco", "evt_p_reco", "user_pop", "frnd_inf1", "evt_pop"]
    )
    X_vec = np.matrix(X_frame)
    y_vec = np.array(data.interested)
    # print(X_vec)
    # print(y_vec)

    # 切分数据集
    cv = cross_validation.ShuffleSplit(len(X_vec), n_iter=10, test_size=0.2, random_state=0)

    # gbdt
    for train, test in cv:
        svc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1).fit(X_vec[train], y_vec[train])
        print("train score: %.3f, test score: %.3f\n" % (
            svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
        ))

    # 画图
    # pyplot.figure()     # 创建1副图
    # pyplot.title("Learning Curve (GDBT)", fontsize=13)
    # pyplot.ylim((0.0, 1.01))
    #
    # # pyplot.xlabel("GDBT")
    # pyplot.ylabel("Score")
    #
    # estimator = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
    # train_size, train_scores, test_scores = learning_curve(
    #     estimator, X_vec, y_vec, cv=cv, n_jobs=16, train_sizes=np.linspace(0.1, 1.0, 5)
    # )  # numpy.linspace()设置曲线刻度
    # train_scores_mean = np.mean(train_scores, axis=1)
    # train_scores_std = np.std(train_scores, axis=1)
    # test_scores_mean = np.mean(test_scores, axis=1)
    # test_scores_std = np.std(test_scores, axis=1)
    # pyplot.grid()  # 显示网格
    # pyplot.fill_between(train_size, train_scores_mean - train_scores_std,
    #                     train_scores_mean + train_scores_std, alpha=0.2, color="r")
    # pyplot.fill_between(train_size, test_scores_mean - test_scores_std,
    #                     test_scores_mean + test_scores_std, alpha=0.2, color="g")
    # pyplot.plot(train_size, train_scores_mean, "o-", color="r", label="Training score")
    # pyplot.plot(train_size, test_scores_mean, "o-", color="g", label="Cross-validation score")
    # pyplot.legend(loc="best")
    #
    # pyplot.show()

def test(clf):
    # 读取test数据，用分类器完成预测
    origTestDf = pd.read_csv(r"D:\kaggle_data\event_recommendation\test.csv")
    users = origTestDf.user
    events = origTestDf.event
    testDf = pd.read_csv("data_test.csv")
    fout = open("result.csv", "w")
    fout.write(",".join(["user", "event", "outcome", "dist"]) + "\n")
    nrows = len(testDf)
    Xp = np.matrix(testDf)
    yp = np.zeros((nrows, 2))
    for i in range(nrows):
        xp = Xp[i, :]
        yp[i, 0] = clf.predict(xp)
        yp[i, 1] = clf.decision_function(xp)
        fout.write(','.join(map(lambda x:str(x), [users[i],events[i],yp[i,0],yp[i,1]])) + "\n")
    fout.close()

def byDist(x, y):
    return int(y[1] - x[1])

def generate_subimtion_file():
    fout = open("final_result.csv", "w")
    fout.write(",".join(["User", "Events"]) + "\n")
    resultDf = pd.read_csv("result.csv")
    grouped = resultDf.groupby("user")
    for name,group in grouped:
        user = str(name)
        tuples = zip(list(group.event), list(group.dist), list(group.outcome))  # list列元素组合
        tuples = sorted(tuples)
        events = "\"" + str(map(lambda x:x[0], tuples)) + "\""
        fout.write(",".join([user,events]) + "\n")
    fout.close()

def result_read():
    # fout = open("final_result2.csv", "w")
    # fout.write(",".join(["User", "Events"]) + "\n")
    resultDf = pd.read_csv("result.csv")
    grouped = resultDf.groupby("user")

    print("user", "[recommend events]")
    for name, group in grouped:
        user = str(name)
        print(name,"," , list(group.event))



if __name__ == "__main__":
    fit_test()
    # validate()
    # clf = train()
    # test(clf)
    # generate_subimtion_file()
    # result_read()
