#coding:utf-8
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import nltk.data
from gensim.models.word2vec import Word2Vec
from nltk.corpus import stopwords

def clean_text(text, remove_stopwords=False):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'[^a-zA-Z]', " ", text)
    words = text.lower().split()
    if remove_stopwords:
        words = [w for w in words if w not in stopwords.words("english")]
    return words

if __name__ == "__main__":
    df = pd.read_csv("./data/unlabeledTrainData_2.csv", header=0)
    print(df.head())

    sentences = [s.split() for s in df.clean_review]

    # 用gensim训练词嵌入模型
    num_features = 300  # Word vector dimensionality
    min_word_count = 40  # Minimum word count
    num_workers = 16  # Number of threads to run in parallel
    context = 10  # Context window size
    downsampling = 1e-3  # Downsample setting for frequent words

    model_name = "{}features_{}minwords_{}context.model".format(num_features,min_word_count,context)

    print("Training model...")
    model = Word2Vec(
        sentences, workers=num_workers,
        size=num_features, min_count=min_word_count,
        window=context, sample=downsampling
    )
    model.init_sims(replace=True)
    model.save(model_name)

    # model_name = "300features_40minwords_10context.model"
    # model = Word2Vec.load(model_name)
    print(model.doesnt_match("man woman child kitchen".split()))
    print(model.doesnt_match("france england germany berlin".split()))
    print(model.most_similar("man"))
    print(model.most_similar("queen"))
    print(model.most_similar("awful"))