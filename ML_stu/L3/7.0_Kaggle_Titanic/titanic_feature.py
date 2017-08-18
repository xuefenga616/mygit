#coding:utf-8
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from matplotlib import pyplot,pylab

# 画图显示中文
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

# jupyter notebook
data_train = pd.read_csv("./train.csv", header=0)
# print(data_train.head())

"""
PassengerId => 乘客ID
Pclass => 乘客等级(1/2/3等舱位)
Name => 乘客姓名
Sex => 性别
Age => 年龄
SibSp => 堂兄弟/妹个数
Parch => 父母与小孩个数
Ticket => 船票信息
Fare => 票价
Cabin => 客舱
Embarked => 登船港口
"""

# print(data_train.info())    # Age（年龄）属性只有714名乘客有记录 Cabin（客舱）更是只有204名乘客是已知的
# print(data_train.describe())    # mean字段告诉我们，大概0.383838的人最后获救了

def plt_01():
    fig = pyplot.figure()
    fig.set(alpha=0.2)                  # 设定图表颜色alpha参数

    pyplot.subplot2grid((2, 3), (0, 0)) #在一张大图里分列几个小图
    data_train.Survived.value_counts().plot(kind="bar")
    pyplot.ylabel(u"获救情况 (1为获救)")
    pyplot.title(u"人数")

    pyplot.subplot2grid((2, 3), (0, 1))
    data_train.Pclass.value_counts().plot(kind="bar")
    pyplot.ylabel(u"人数")
    pyplot.title(u"乘客等级分布")

    pyplot.subplot2grid((2, 3), (0, 2))
    pyplot.scatter(data_train.Survived, data_train.Age)
    pyplot.ylabel(u"年龄")
    pyplot.grid(b=True, which="major", axis="y")
    pyplot.title(u"按年龄看获救分布 (1为获救)")

    pyplot.subplot2grid((2, 3), (1, 0), colspan=2)
    data_train.Age[data_train.Pclass==1].plot(kind="kde")
    data_train.Age[data_train.Pclass==2].plot(kind="kde")
    data_train.Age[data_train.Pclass==3].plot(kind="kde")
    pyplot.xlabel(u"年龄")
    pyplot.xlabel(u"密度")
    pyplot.title(u"各等级的乘客年龄分布")
    pyplot.legend((u'头等舱', u'2等舱',u'3等舱'), loc="best")

    pyplot.subplot2grid((2, 3), (1, 2))
    data_train.Embarked.value_counts().plot(kind="bar")
    pyplot.title(u"各登船口岸上船人数")
    pyplot.ylabel(u"人数")

    pyplot.show()

def plt_02():
    fig = pyplot.figure()
    fig.set(alpha=0.2)      # 设定图表颜色alpha参数，透明度

    Survived_0 = data_train.Pclass[data_train.Survived==0].value_counts()
    Survived_1 = data_train.Pclass[data_train.Survived==1].value_counts()
    df = pd.DataFrame({u"获救": Survived_1, u"未获救": Survived_0})
    df.plot(kind="bar", stacked=True)
    pyplot.title(u"各乘客等级的获救情况")
    pyplot.xlabel(u"乘客等级")
    pyplot.ylabel(u"人数")

    pyplot.show()

def plt_03():
    fig = pyplot.figure()
    fig.set(alpha=0.2)

    Survived_0 = data_train.Embarked[data_train.Survived==0].value_counts()
    Survived_1 = data_train.Embarked[data_train.Survived==1].value_counts()
    df = pd.DataFrame({u"获救": Survived_1, u"未获救": Survived_0})
    df.plot(kind="bar", stacked=True)
    pyplot.title(u"各登陆港口乘客的获救情况")
    pyplot.xlabel(u"登陆港口")
    pyplot.ylabel(u"人数")

    pyplot.show()

def plt_04():
    fig = pyplot.figure()
    fig.set(alpha=0.2)

    Survived_m = data_train.Survived[data_train.Sex=="male"].value_counts()
    Survived_f = data_train.Survived[data_train.Sex=="female"].value_counts()
    df = pd.DataFrame({u"男性": Survived_m, u"女性": Survived_f})
    df.plot(kind="bar", stacked=True)
    pyplot.title(u"按性别看获救情况")
    pyplot.xlabel(u"性别")
    pyplot.ylabel(u"人数")

    pyplot.show()

def plt_05():
    fig = pyplot.figure()
    fig.set(alpha=0.65)
    pyplot.title(u"根据舱等级和性别的获救情况")

    ax1 = fig.add_subplot(141)
    data_train.Survived[data_train.Sex == "female"][data_train.Pclass != 3].value_counts().plot(kind="bar",
                                                                                                label="female highclass",
                                                                                                color="#FA2479")
    ax1.set_xticklabels([u"获救", u"未获救"], rotation=0)
    ax1.legend([u"女性/高级舱"], loc="best")

    ax2 = fig.add_subplot(142, sharey=ax1)
    data_train.Survived[data_train.Sex == "female"][data_train.Pclass == 3].value_counts().plot(kind="bar",
                                                                                                label="female lowclass",
                                                                                                color="pink")
    ax2.set_xticklabels([u"未获救", u"获救"], rotation=0)
    ax2.legend([u"女性/低级舱"], loc="best")

    ax3 = fig.add_subplot(143, sharey=ax1)
    data_train.Survived[data_train.Sex == "male"][data_train.Pclass != 3].value_counts().plot(kind="bar",
                                                                                                label="male highclass",
                                                                                                color="lightblue")
    ax3.set_xticklabels([u"未获救", u"获救"], rotation=0)
    ax3.legend([u"女性/高级舱"], loc="best")

    ax4 = fig.add_subplot(144, sharey=ax1)
    data_train.Survived[data_train.Sex == "male"][data_train.Pclass == 3].value_counts().plot(kind="bar",
                                                                                                label="male lowclass",
                                                                                                color="steelblue")
    ax4.set_xticklabels([u"未获救", u"获救"], rotation=0)
    ax4.legend([u"男性/低级舱"], loc="best")

    pyplot.show()

def plt_06():
    g = data_train.groupby(["SibSp", "Survived"])
    df = pd.DataFrame(g.count()["PassengerId"])     # 只显示乘客id
    # print(df)

    g = data_train.groupby(["Parch", "Survived"])
    df = pd.DataFrame(g.count()["PassengerId"])
    # print(df)

    # print(data_train.Cabin.value_counts())

    fig = pyplot.figure()
    fig.set(alpha=0.2)
    Survived_cabin = data_train.Survived[pd.notnull(data_train.Cabin)].value_counts()
    Survived_nocabin = data_train.Survived[pd.isnull(data_train.Cabin)].value_counts()
    df = pd.DataFrame({u"有": Survived_cabin, u"无": Survived_nocabin}).transpose()   # transpose()平移
    df.plot(kind="bar", stacked=True)
    pyplot.title(u"按Cabin有无看获救情况")
    pyplot.xlabel(u"Cabin有无")
    pyplot.ylabel(u"人数")
    pyplot.show()

if __name__ == "__main__":
    plt_01()