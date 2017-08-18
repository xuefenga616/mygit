#coding:utf-8
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import re

def predict_next(input_array):
    X = np.reshape(input_array, (1, seq_length, 1))
    X = X/float(n_vocab)
    y = model.predict(X)
    return y

def string_to_index(raw_input):
    res = []
    for c in raw_input[(len(raw_input) - seq_length): ]:
        res.append(char_to_int[c])
    return res

def y_to_char(y):
    c = int_to_char[y.argmax()]
    return c

def generate_article(init, rounds=500):
    in_string = init.lower()
    for i in range(rounds):
        n = y_to_char(predict_next(string_to_index(in_string)))
        in_string += n
    return in_string

if __name__ == "__main__":
    # 读入文本
    raw_text = open("./data/Winston_Churchil.txt").read()
    raw_text = re.sub(r'[^\x00-\x7f]+', ' ', raw_text).lower()   # 去掉所有非英文字符

    chars = sorted(set(raw_text))
    print(chars)
    print(len(chars), len(raw_text))
    char_to_int = dict((c,i) for i,c in enumerate(chars))
    int_to_char = dict((i,c) for i,c in enumerate(chars))

    # 把raw text变成可以用来训练的x,y
    seq_length = 100
    X = []
    y = []
    for i in range(len(raw_text) - seq_length):
        given = raw_text[i: i+seq_length]   # 扫描框
        predict = raw_text[i+seq_length]
        X.append([char_to_int[char] for char in given])
        y.append(char_to_int[predict])
    # print(X[:3])
    # print(y[:3])

    n_patterns = len(X)
    n_vocab = len(chars)
    # 把X变成LSTM需要的样子
    X = np.reshape(X, (n_patterns, seq_length, 1))
    # 简单normal到0-1之间
    X = X / float(n_vocab)
    # output变成one-hot
    y = np_utils.to_categorical(y)
    # print(X[10])
    # print(y[10])

    # LSTM模型构建
    model = Sequential()    # 序贯模型
    model.add(LSTM(128, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam")

    # 跑模型
    model.fit(X, y, nb_epoch=10, batch_size=32)

    # 开始写文章
    init = "Professor Michael S. Hart is the originator of the Project"
    article = generate_article(init)
    print(article)