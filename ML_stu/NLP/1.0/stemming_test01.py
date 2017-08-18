#coding:utf-8
from nltk.stem.porter import PorterStemmer  # 词干提取
porter_stemmer = PorterStemmer()
print(porter_stemmer.stem("maximum"))
print(porter_stemmer.stem("presumably"))
print(porter_stemmer.stem("multiply"))
print(porter_stemmer.stem("provision"))
print("\n")

from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer("english")
print(snowball_stemmer.stem("maximum"))
print(snowball_stemmer.stem("presumably"))
print("\n")

from nltk.stem.lancaster import LancasterStemmer
lancaster_stemmer = LancasterStemmer()
print(lancaster_stemmer.stem("maximum"))
print(lancaster_stemmer.stem("presumably"))