#coding:utf-8
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from matplotlib import pyplot
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn import linear_model

# jupyter notebook


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

# 使用RandomForestRegressor填补缺失的年龄属性
def set_missing_ages(df):
    # 把已有的数值型特征取出丢进RandomForestRegressor中
    age_df = df[["Age", "Fare", "Parch", "SibSp", "Pclass"]]

    # 乘客分成已知年龄和未知年龄两部分
    known_age = age_df[age_df.Age.notnull()].as_matrix()    # as_matrix() 把vector或data frame转换成矩阵
    unknown_age = age_df[age_df.Age.isnull()].as_matrix()

    # y即目标年龄
    y = known_age[:, 0]

    # X即特征属性值
    X = known_age[:, 1:]

    # fit到RandomForestRegressor中
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)

    # 用得到的模型进行未知年龄结果预测
    predictAges = rfr.predict(unknown_age[:, 1:])

    # 用得到的预测结果填补原缺失数据
    df.loc[(df.Age.isnull()), "Age"] = predictAges

    return df, rfr

def set_Cabin_type(df):
    df.loc[(df.Cabin.notnull()), "Cabin"] = "Yes"
    df.loc[(df.Cabin.isnull()), "Cabin"] = "No"

    return df

def data_handler(data_train):
    data_train, rfr = set_missing_ages(data_train)
    data_train = set_Cabin_type(data_train)
    # print(data_train.head())

    # 因为逻辑回归建模时，需要输入的特征都是数值型特征
    # 我们先对类目型的特征离散/因子化
    # 以Cabin为例，原本一个属性维度，因为其取值可以是['yes','no']，而将其平展开为'Cabin_yes','Cabin_no'两个属性
    # 原本Cabin取值为yes的，在此处的'Cabin_yes'下取值为1，在'Cabin_no'下取值为0
    # 原本Cabin取值为no的，在此处的'Cabin_yes'下取值为0，在'Cabin_no'下取值为1
    # 我们使用pandas的get_dummies来完成这个工作，并拼接在原来的data_train之上，如下所示
    dummies_Cabin = pd.get_dummies(data_train["Cabin"], prefix="Cabin")
    dummies_Embarked = pd.get_dummies(data_train["Embarked"], prefix="Embarked")
    dummies_Sex = pd.get_dummies(data_train["Sex"], prefix="Sex")
    dummies_Pclass = pd.get_dummies(data_train["Pclass"], prefix="Pclass")
    df = pd.concat([data_train, dummies_Cabin, dummies_Embarked, dummies_Sex, dummies_Pclass], axis=1)  # 拼接
    df.drop(["Pclass", "Name", "Sex", "Ticket", "Cabin", "Embarked"], axis=1, inplace=True)
    # print(df.head())

    # 用preprocessing处理连续值：均值为0，方差为1
    scaler = preprocessing.StandardScaler()
    age_scaler_param = scaler.fit(df["Age"])
    df["Age_scaled"] = scaler.fit_transform(df["Age"], age_scaler_param)
    fare_scale_param = scaler.fit(df["Fare"])
    df["Fare_scaled"] = scaler.fit_transform(df["Fare"], fare_scale_param)
    # print(df.head())

    return df

if __name__ == "__main__":
    data_train = pd.read_csv("./train.csv", header=0)
    # print(data_train.head())
    df = data_handler(data_train)
    train_df = df.filter(regex="Survived|Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*")
    # print(train_df.head())
    train_np = train_df.as_matrix()

    y = train_np[:, 0]
    X = train_np[:, 1:]
    clf = linear_model.LogisticRegression(C=1.0, penalty="l1", tol=1e-6)    # C是正则化项参数
    clf.fit(X, y)   # 训练
    print(clf)

    data_test = pd.read_csv("./test.csv", header=0)
    data_test.loc[(data_test.Fare.isnull()), "Fare"] = 0
    df_test = data_handler(data_test)
    test_df = df_test.filter(regex="Age_.*|SibSp|Parch|Fare_.*|Cabin_.*|Embarked_.*|Sex_.*|Pclass_.*")
    predictions = clf.predict(test_df)

    result = pd.DataFrame({"PassengerId": data_test["PassengerId"].as_matrix(), "Survived": predictions.astype(np.int32)})
    print(result)