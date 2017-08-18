#coding:utf-8
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing

data = pd.read_csv("./kaggle_bike_competition_train.csv", header=0, error_bad_lines=False)
# print(data.head())

# 处理时间字段
temp_datetime = pd.DatetimeIndex(data["datetime"])
data["date"] = temp_datetime.date
# data["time"] = temp_datetime.time
data["hour"] = pd.to_datetime(temp_datetime.time, format="%H:%M:%S")
data["hour"] = pd.Index(data["hour"]).hour

data["dayofweek"] = pd.DatetimeIndex(data.date).dayofweek               # 星期几
data["dateDays"] = (data.date - data.date[0]).astype("timedelta64[D]")  # 产出一个时间长度（猜测越往后骑车的越多）
# print(data.head())

byday = data.groupby("dayofweek")
# print(byday["casual"].sum().reset_index())      # 统计没注册的用户租赁情况
# print(byday["registered"].sum().reset_index())  # 统计注册的

# 周末既然有不同，就单独拿2列出来分别给周六、日
data["Saturday"] = 0
data["Sunday"] = 0
data.Saturday[data.dayofweek==5] = 1
data.Sunday[data.dayofweek==6] = 1

# 从数据中，把原始的时间字段等剔除
dateRel = data.drop(["datetime", "count", "date", "dayofweek"], axis=1)     # axis=1代表列项
print(dateRel.head())

# 把连续值得属性放入1个dict中
featureConCols = ["temp", "atemp", "humidity", "windspeed", "dateDays", "hour"]
dataFeatureCon = dateRel[featureConCols]
dataFeatureCon = dataFeatureCon.fillna("NA")
X_dictCon = dataFeatureCon.T.to_dict().values()

# 把离散值得属性放到另一个dict中
featureCatCols = ["season", "holiday", "workingday", "weather", "Saturday", "Sunday"]
dataFeatureCat = dateRel[featureCatCols]
dataFeatureCat = dataFeatureCat.fillna("NA")
X_dictCat = dataFeatureCat.T.to_dict().values()

# 向量化特征
vec = DictVectorizer(sparse=False)
X_vec_cat = vec.fit_transform(X_dictCat)
X_vec_con = vec.fit_transform(X_dictCon)
# print(dataFeatureCon.head())
# print(X_vec_con)
# print(dataFeatureCat.head())
# print(X_vec_cat)

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
print(X_vec)

# 对y向量化
Y_vec_reg = dateRel["registered"].values.astype(float)
Y_vec_cas = dateRel["casual"].values.astype(float)
print(Y_vec_reg)
print(Y_vec_cas)