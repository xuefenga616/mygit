#coding:utf-8
from nltk.stem import WordNetLemmatizer     # 词性归一
wordnet_lemmatizer = WordNetLemmatizer()
print(wordnet_lemmatizer.lemmatize("dogs"))
print(wordnet_lemmatizer.lemmatize("churches"))
print(wordnet_lemmatizer.lemmatize("aardwolves"))
print(wordnet_lemmatizer.lemmatize("abaci"))
print(wordnet_lemmatizer.lemmatize("hardrock"))

# 没有pso tag，默认是NN 名词
print(wordnet_lemmatizer.lemmatize("are"))
print(wordnet_lemmatizer.lemmatize("is"))
# 加上pos tag
print(wordnet_lemmatizer.lemmatize("are", pos="v"))
print(wordnet_lemmatizer.lemmatize("is", pos="v"))
print("\n")

import nltk
text = nltk.word_tokenize("what does the fox say")
print(text)
print(nltk.pos_tag(text))

