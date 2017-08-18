#coding:utf-8
from nltk import FreqDist
import nltk

# 做个词库
corpus = '''
    this is my sentence
    this is my life
    this is the day
'''

tokens = nltk.word_tokenize(corpus)
# print(tokens)

# 使用FreqDist统计一下文字出现的频率
fdist = FreqDist(tokens)
print(fdist['is'])  # 统计'is'出现的次数

# 把最常出现的50个单词拿出来
standard_freq_vector = fdist.most_common(50)
size = len(standard_freq_vector)
print(standard_freq_vector)

# 按照出现频率的大小，记录下每个单词的位置
def position_lookup(v):
    res = {}
    counter = 0
    for word in v:
        res[word[0]] = counter
        counter += 1
    return res
standard_position_dict = position_lookup(standard_freq_vector)
# print(standard_position_dict)

# 这时有个新句子，新建一个跟我们的标准vector同样大小的向量
sentence = "this is cool"
freq_vector = [0] * size
tokens = nltk.word_tokenize(sentence)
for word in tokens:
    try:
        freq_vector[standard_position_dict[word]] += 1
    except:
        continue    # 如果是新词就pass掉

print(freq_vector)
