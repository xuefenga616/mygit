#coding:utf-8
from nltk.text import TextCollection
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 把所有的文档放到TextCollection类中，
# 这个类会自动帮你断句，做统计，做计算
corpus = [
    'this is sentence one',
    'this is sentence two',
    'this is sentence three',
    'this is sentence four',
    'this is sentence five'
]

vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值

#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
# print(tfidf)
word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
print(weight)
