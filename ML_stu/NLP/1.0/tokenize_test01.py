#coding:utf-8
# import nltk
# sentence = "hello, world"
# tokens = nltk.word_tokenize(sentence)
# print(tokens)


# import jieba
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# # seg_list = jieba.cut("今天天气真不错", cut_all=False)
# print("Default Mode:", "/".join(seg_list))
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode:", "/".join(seg_list))
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")
# print(",".join(seg_list))

from nltk.tokenize import word_tokenize
import re
tweet = 'RT @angelababy: love you baby! :D http://ah.love #168cm'
# print(word_tokenize(tweet))
# ?:只是用来分组，不会占用捕获变量；只有?表示非贪婪模式
emoticons_str = r"""    
(?:
    [:=;]       # 眼睛
    [o0\-]?     # 鼻子
    [D\)\]\(\]/\\OpP]   # 嘴
)
"""
regex_str = [
    emoticons_str,
    r'<[^>]+>',         # html tags
    r'(?:@[\w_]+)',     # @某人
    r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',   # 话题标签
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',   #urls
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',   # 数字
    r"(?:[a-z][a-z'\-_]+[a-z])",    # 含有-和'的单词
    r'(?:[\w_]+)',      # 其他
    r'(?:\S)'           #其他
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE|re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE|re.IGNORECASE)
def tokenize(s):
    return tokens_re.findall(s)
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [t if emoticon_re.search(t) else t.lower() for t in tokens]
    return tokens
print(preprocess(tweet))