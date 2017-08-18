#coding:utf-8
import numpy as np
import nltk
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from gensim.models.word2vec import Word2Vec
import re

def predict_next(input_array):
    x = np.reshape(input_array, (-1,seq_length,128))
    y = model.predict(x)
    return y

def string_to_index(raw_input):
    raw_input = raw_input.lower()
    input_stream = nltk.word_tokenize(raw_input)

    res = []
    for word in input_stream[(len(input_stream)-seq_length):]:
        res.append(w2v_model[word])
    return res

def y_to_word(y):
    word = w2v_model.most_similar(positive=y, topn=1)
    return word

def generate_article(init, rounds=30):
    in_string = init.lower()
    for i in range(rounds):
        n = y_to_word(predict_next(string_to_index(in_string)))
        in_string += ' ' + n[0][0]
    return in_string

if __name__ == "__main__":
    # 读入文本
    raw_text = open("./data/Winston_Churchil.txt").read()
    raw_text = re.sub(r'[^\x00-\x7f]+', ' ', raw_text).lower()  # 去掉所有非英文字符

    # 分词
    corpus = []
    for sen in raw_text.split("."):
        sen = sen.strip() + "."     # 把句号加上
        corpus.append(nltk.word_tokenize(sen))
    # print(len(corpus))
    # print(corpus[:3])

    # word2vec建模
    w2v_model = Word2Vec(corpus, size=128, window=5, min_count=5, workers=16)   # size表示词向量长度
    # print(w2v_model["office"])

    # 把源数据变成一个长长的X，好让LSTM学习
    raw_input = [item for sublist in corpus for item in sublist]
    # print(len(raw_input))

    text_stream = [word for word in raw_input if word in w2v_model]
    # print(len(text_stream))
    # print(text_stream[10])

    seq_length = 10
    X = []
    y = []
    for i in range(len(text_stream) - seq_length):
        given = text_stream[i: i + seq_length]
        predict = text_stream[i + seq_length]
        X.append(np.array([w2v_model[word] for word in given]))
        y.append(w2v_model[predict])
    print(X[10])
    print(y[10])

    # 把X变成LSTM需要的数组格式：样本数、时间步伐、特征
    # 对于output，直接用128维的输出
    X = np.reshape(X, (-1, seq_length, 128))
    y = np.reshape(y, (-1, 128))

    # LSTM建模
    model = Sequential()
    model.add(LSTM(256, dropout_W=0.2, dropout_U=0.2, input_shape=(seq_length, 128)))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='sigmoid'))
    model.compile(loss='mse', optimizer='adam')

    model.fit(X, y ,nb_epoch=50, batch_size=4096)

    init = 'Patriotic as Churchill was, he managed to maintain a balanced in his description of the war'
    article = generate_article(init)
    print(article)