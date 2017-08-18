#coding:utf-8
import re
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from datetime import date
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer # 词性归一
from gensim.models.word2vec import Word2Vec
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Convolution2D,MaxPooling2D
from keras.layers.core import Dense,Dropout,Activation,Flatten

def preprocessing(sen):
    res = []
    for word in sen:
        w = word.lower().replace("b'", "").replace('b"', "")
        w = re.sub(r"[^a-zA-Z]", "", w)
        # if w and w not in stopwords.words("english"):
        if w:
            res.append(WordNetLemmatizer().lemmatize(w))
    return res

def get_vector(word_list):
    res = np.zeros([128])
    cnt = 0
    for word in word_list:
        if word in model:
            res += model[word]
            cnt += 1
    return res/cnt

# 对于每天的新闻，考虑前256个单词。不够的用[00000]补上
def transform_to_matrix(x, padding_size=256, vec_size=128):
    res = []
    for sen in x:
        matrix = []
        for i in range(padding_size):
            try:
                matrix.append(model[sen[i]].tolist())
            except:
                matrix.append([0]*vec_size)
        res.append(matrix)
    return res

if __name__ == "__main__":
    data = pd.read_csv("./stocknews/Combined_News_DJIA.csv")
    # print(data.head())

    # 把数据分成training/testing data
    train = data[data['Date'] < '2015-01-01']
    test = data[data['Date'] >= '2015-01-01']
    # print(train.describe())
    # print(test.describe())

    # 把每条新闻做成一个单独的句子，集合在一起
    X_train = train[train.columns[2:]]
    # corpus是全部的文本资料
    corpus = X_train.values.flatten().astype(str)
    # print(corpus[:3])

    X_train = X_train.values.astype(str)
    X_train = np.array([' '.join(x) for x in X_train])  # 每行top25合并成一句话
    # print(len(X_train))
    y_train = train["Label"].values

    X_test = test[test.columns[2:]]
    X_test = X_test.values.astype(str)
    X_test = np.array([' '.join(x) for x in X_test])
    y_test = test["Label"].values

    # 分词及其他预处理
    corpus = [preprocessing(word_tokenize(x)) for x in corpus]
    X_train = [preprocessing(word_tokenize(x)) for x in X_train]
    X_test = [preprocessing(word_tokenize(x)) for x in X_test]
    # print(corpus[553])
    # print(X_train[523])

    # w2c模型
    model = Word2Vec(corpus, size=128, window=5, min_count=5, workers=16)
    # print(model["ok"])

    # # 均值化每个句子为向量
    # X_train = [get_vector(x) for x in X_train]
    # X_test = [get_vector(x) for x in X_test]
    # # print(X_train[10])
    #
    # # SVM建模
    # clf = SVR(C=10, gamma=10).fit(X_train, y_train)
    # # test_score = cross_val_score(clf, X_train, y_train, cv=10, scoring="roc_auc")
    # print("train score: %.3f, test score: %.3f\n" % (
    #     clf.score(X_train, y_train), clf.score(X_test, y_test)
    # ))

    # 开始用CNN的模型跑一跑
    X_train = transform_to_matrix(X_train)
    X_test = transform_to_matrix(X_test)
    # print(X_train[123])
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1], X_train.shape[2])
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1], X_test.shape[2])
    print(X_train.shape)
    print(X_test.shape)

    # set parameters
    batch_size = 32
    n_filter = 16
    filter_length = 4
    nb_epoch =5
    n_pool =2

    # 新建一个sequential的模型
    model = Sequential()
    model.add(Convolution2D(n_filter, filter_length, filter_length, input_shape=(1, 256, 128)))
    # model.add(Convolution2D(n_filter, filter_length, filter_length))
    model.add(Activation('relu'))
    model.add(Convolution2D(n_filter, filter_length, filter_length))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(n_pool, n_pool)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    # 后面接上一个ANN
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('softmax'))
    # compile模型
    model.compile(loss='mse',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch, verbose=0)
    score = model.evaluate(X_test, y_test, verbose=0)
    print("Test score: ", score[0])
    print("Test accuracy: ", score[1])