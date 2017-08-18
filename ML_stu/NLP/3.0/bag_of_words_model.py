#coding:utf-8
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import nltk
from nltk.corpus import stopwords

def display(text, title):
    print(title)
    print("分割线".center(50, "-"))
    print(text)

def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.lower().split()
    # words = [w for w in words if w not in stopwords.words("english")]
    return ' '.join(words)

if __name__ == "__main__":
    # datafile = "./data/testData.tsv"
    # df = pd.read_csv(datafile, sep="\t", escapechar="\\")
    # # print(df.head())
    #
    # raw_example = df['review'][1]
    # # raw_example = BeautifulSoup(raw_example, "html.parser").get_text()
    # # display(raw_example, "去掉html标签的数据")
    # # example_letters = re.sub(r'[^a-zA-Z]', ' ', raw_example)    # 将非字符替换为" "
    # # display(example_letters, "去掉标点的数据")
    # # words = example_letters.lower().split()
    # # display(words, "纯词列表数据")
    # #
    # # words_nostop = [w for w in words if w not in stopwords.words("english")]
    # # display(words_nostop, "去掉停用词数据")
    #
    # # print(clean_text(raw_example))
    # df['clean_review'] = df.review.apply(clean_text)    # review后添加1列处理过的评论特征
    # # print(df.head())
    # output = pd.DataFrame({'id':df.id, 'clean_review':df.clean_review})
    # output.to_csv("./data/testData_2.csv", index=False)
    # print(df.head())

    datafile = "./data/labeledTrainData_2.csv"
    df = pd.read_csv(datafile, header=0)
    # print(df.head())

    # 提取bag of words特征
    vectorizer = CountVectorizer(max_features=5000)
    train_data_features = vectorizer.fit_transform(df.clean_review).toarray()
    # print(train_data_features.shape)

    # 训练分类器
    forest = RandomForestClassifier(n_estimators=100)
    clf = forest.fit(train_data_features, df.sentiment)

    # 读取测试数据进行预测
    datafile = "./data/testData_2.csv"
    df = pd.read_csv(datafile, header=0)
    # df['clean_review'] = df.review.apply(clean_text)
    print(df.head())

    test_data_features = vectorizer.transform(df.clean_review).toarray()
    print(test_data_features.shape)

    result = clf.predict(test_data_features)
    output = pd.DataFrame({'id': df.id, 'sentiment':result})
    print(output.head())
    output.to_csv("./data/Bag_of_Words_model.csv", index=False)

