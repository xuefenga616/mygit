#coding:utf-8
import numpy as np
import pandas as pd
from matplotlib import pyplot
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier
from sklearn.learning_curve import learning_curve

# jupyter notebook
def train_preprocess():
    # 下采样
    data = pd.read_csv(r"D:\kaggle_data\CTR\avazu-ctr-prediction\train.csv", nrows=100000)
    data_0 = data[data.click==0]
    data_1 = data[data.click==1]
    data_0_ed = data_0[:len(data_1)]
    data_downSampled = pd.concat([data_1, data_0_ed])

    list_param = ['C1', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'banner_pos', 'device_type',
                  'device_conn_type', 'click']
    # print(data["C18"].describe())
    # print(data[list_param].head(10))

    # 寻找相关特征
    fig, axs = pyplot.subplots(3, 3, sharey=True)
    fig.set(alpha=0.65)

    click_pos_0 = data.click[data.banner_pos==0].value_counts()
    click_pos_1 = data.click[data.banner_pos==1].value_counts()
    df1 = pd.DataFrame({"pos0": click_pos_0, "pos1": click_pos_1}).transpose()  # transpose()平移
    df1.plot(kind="bar", stacked=True, ax=axs[0,0], figsize=(16,8))
    pyplot.ylabel("Count")

    device_0 = data.click[data.device_type==0].value_counts()
    device_1 = data.click[data.device_type==1].value_counts()
    device_4 = data.click[data.device_type==4].value_counts()
    df2 = pd.DataFrame({"dev0": device_0, "dev1": device_1, "dev4": device_4}).transpose()
    df2.plot(kind="bar", stacked=True, ax=axs[0,1])

    conn_0 = data.click[data.device_conn_type == 0].value_counts()
    conn_2 = data.click[data.device_conn_type == 2].value_counts()
    conn_3 = data.click[data.device_conn_type == 3].value_counts()
    df3 = pd.DataFrame({"conn0": conn_0, "conn2": conn_2, "conn3": conn_3}).transpose()
    df3.plot(kind="bar", stacked=True, ax=axs[0, 2])

    c1_0 = data.click[data.C1 == 1005].value_counts()
    c1_5 = data.click[data.C1 == 1010].value_counts()
    df4 = pd.DataFrame({"1005": c1_0, "1010": c1_5}).transpose()
    df4.plot(kind="bar", stacked=True, ax=axs[1, 0])

    c18_0 = data.click[data.C18 == 0].value_counts()
    c18_2 = data.click[data.C18 == 2].value_counts()
    c18_3 = data.click[data.C18 == 3].value_counts()
    df5 = pd.DataFrame({"0": c18_0, "2": c18_2, "3": c18_3}).transpose()
    df5.plot(kind="bar", stacked=True, ax=axs[1, 1])

    c20_0 = data.click[data.C20 == -1].value_counts()
    c20_1 = data.click[data.C20 != -1].value_counts()
    df6 = pd.DataFrame({"null": c20_0, "fit": c20_1}).transpose()
    df6.plot(kind="bar", stacked=True, ax=axs[1, 2])

    # pyplot.show()

    data_downSampled_1 = data_downSampled[list_param]
    # 打乱数据
    sampler = np.random.permutation(len(data_downSampled_1))
    data_downSampled_1 = data_downSampled_1.take(sampler)

    # print(data_downSampled_1.head(10))
    # print(data_downSampled_1.count())
    # data_downSampled_1.to_csv("train_small.csv")

def test_preprocess():
    test_df = pd.read_csv(r"D:\kaggle_data\CTR\avazu-ctr-prediction\test.csv")
    list_param = ['id', 'C1', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'banner_pos', 'device_type',
                  'device_conn_type']
    test_small = test_df[list_param]
    test_small = test_small.to_csv("test_small.csv")
    print(test_small.head(10))

def feature_generate():
    data = pd.read_csv("train_small.csv", nrows=100000)

    # 处理C20
    data.loc[(data.C20!=-1), "C20"] = "Yes"
    data.loc[(data.C20==-1), "C20"] = "No"
    print(data.head(10))

    # 处理连续值
    featureConCols = ["C14", "C17", "C21"]
    dataFeatureCon = data[featureConCols]
    # dataFeatureCon = dataFeatureCon.fillna("NA")
    X_dictCon = dataFeatureCon.T.to_dict().values()

    # 处理离散值
    featureCatCols = ["C1", "C15", "C16", "C18", "C19", "C20", "banner_pos", "device_type", "device_conn_type"]
    dataFeatureCat = data[featureCatCols]
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
    # print(X_vec.shape)

    y_vec = data["click"].values.astype(float)

    return X_vec, y_vec

def fit(X_vec, y_vec):
    # 切分数据集
    cv = cross_validation.ShuffleSplit(len(X_vec), n_iter=10, test_size=0.2, random_state=0)

    # 随机森林回归
    # for train, test in cv:
    #     svc = RandomForestClassifier(n_estimators=100).fit(X_vec[train], y_vec[train])
    #     print("train score: %.3f, test score: %.3f\n" % (
    #         svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
    #     ))

    # gbdt
    # for train, test in cv:
    #     svc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1).fit(X_vec[train], y_vec[train])
    #     print("train score: %.3f, test score: %.3f\n" % (
    #         svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
    #     ))

    # xgboost
    for train, test in cv:
        svc = XGBClassifier(max_depth=10, gamma=0.001).fit(X_vec[train], y_vec[train])
        print("train score: %.3f, test score: %.3f\n" % (
            svc.score(X_vec[train], y_vec[train]), svc.score(X_vec[test], y_vec[test])
        ))

def starckModel(X_vec, y_vec):
    # 切分数据集
    # train_X, test_X, train_y, test_y = train_test_split(X_vec, y_vec, test_size=0.2)
    cv = cross_validation.ShuffleSplit(len(X_vec), n_iter=10, test_size=0.2, random_state=0)

    clfs = [
        RandomForestClassifier(n_estimators=100),
        GradientBoostingClassifier(n_estimators=100, learning_rate=0.1),
        XGBClassifier(max_depth=10, gamma=0.001)
    ]

    for train, test in cv:
        data_stack_train = np.zeros((X_vec[train].shape[0], len(clfs)))
        data_stack_test = np.zeros((X_vec[test].shape[0], len(clfs)))
        for j,clf in enumerate(clfs):
            clf.fit(X_vec[train], y_vec[train])
            y_submission = clf.predict(X_vec[test])
            y_train = clf.predict(X_vec[train])
            data_stack_train[:,j] = y_train
            data_stack_test[:,j] = y_submission
        #########
        svc = RandomForestClassifier(n_estimators=100, max_depth=10).fit(data_stack_train, y_vec[train])
        print("train score: %.3f, test score: %.3f\n" % (
            svc.score(data_stack_train, y_vec[train]), svc.score(data_stack_test, y_vec[test])
        ))

def plotCurve(title, estimator, X, y, ylim=None, cv=None):
    # title = "Learning Curves (Random Forest, n_estimators = 100)"
    # pyplot.figure()     # 创建1副图
    # pyplot.subplot2grid((3, 3), (1, 2), rowspan=1, colspan=1)
    # pyplot.title(title)
    if ylim is not None:
        pyplot.ylim(*ylim)

    pyplot.xlabel(title, fontsize=13)
    # pyplot.ylabel("Score")

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

    # pyplot.show()


if __name__ == "__main__":
    train_preprocess()
    # test_preprocess()
    X_vec,y_vec = feature_generate()
    # fit(X_vec, y_vec)
    # starckModel(X_vec, y_vec)

    cv = cross_validation.ShuffleSplit(X_vec.shape[0], n_iter=10, test_size=0.2, random_state=0)
    estimator1 = RandomForestClassifier(n_estimators=100, max_depth=10)
    title1 = "Learning Curves (Random Forest)"
    pyplot.subplot2grid((3, 3), (2, 0), rowspan=1, colspan=1)
    plotCurve(title1, estimator1, X_vec, y_vec, (0.0, 1.01), cv=cv)  # ylim设置y轴范围

    estimator2 = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
    title2 = "GBDT"
    pyplot.subplot2grid((3, 3), (2, 1), rowspan=1, colspan=1)
    plotCurve(title2, estimator2, X_vec, y_vec, (0.0, 1.01), cv=cv)

    estimator3 = XGBClassifier(max_depth=10, gamma=0.001)
    title3 = "xgboost"
    pyplot.subplot2grid((3, 3), (2, 2), rowspan=1, colspan=1)
    plotCurve(title3, estimator3, X_vec, y_vec, (0.0, 1.01), cv=cv)

    pyplot.show()




