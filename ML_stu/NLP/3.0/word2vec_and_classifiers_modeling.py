#coding:utf-8
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from gensim.models.word2vec import Word2Vec
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.cluster import KMeans
from nltk.corpus import stopwords

def to_review_vector(review):
    words = review.split()
    # words = [w for w in review.split() if w not in stopwords.words("english")]
    # 根据word2vec的结果对影评文本进行编码
    # 把这句话中的词的词向量做平均
    array = np.array([model[w] for w in words if w in model])
    return pd.Series(array.mean(axis=0))    # 水平方向

if __name__ == "__main__":
    model = Word2Vec.load("300features_40minwords_10context.model")
    df = pd.read_csv("./data/labeledTrainData_2.csv", header=0)
    # print(df.head())

    train_data_features = df.clean_review.apply(to_review_vector)
    # print(train_data_features.head())

    forest = RandomForestClassifier(n_estimators=100, random_state=42)
    clf = forest.fit(train_data_features, df.sentiment)

    # 同样在训练集上试试，确保模型能正常work
    print(confusion_matrix(df.sentiment, clf.predict(train_data_features)))

    df = pd.read_csv("./data/testData_2.csv", header=0)
    print(df.head())
    test_data_features = df.clean_review.apply(to_review_vector)

    result = clf.predict(test_data_features)
    output = pd.DataFrame({'id':df.id, 'sentiment':result})
    output.to_csv("./data/Word2Vec_model.csv", index=False)
    print(output.head())