#coding:utf-8
# sentiment_dict = {}
# for line in open('data/AFINN-111.txt'):
#     word, score = line.split('\t')
#     sentiment_dict[word] = int(score)
#
# total_score = sum(sentiment_dict.get(word,0) for word in words)
# # 有值就是dict中的值，没有就是0


from nltk.classify import NaiveBayesClassifier
s1 = 'this is a good book'
s2 = 'this is a awesome book'
s3 = 'this is a bad book'
s4 = 'this is a terrible book'

def preprocess(s):
    return {word: True for word in s.lower().split()}

training_data = [
    [preprocess(s1), "pos"],
    [preprocess(s2), "pos"],
    [preprocess(s3), "neg"],
    [preprocess(s4), "neg"]
]
model = NaiveBayesClassifier.train(training_data)
print(model.classify(preprocess("this is a good book")))