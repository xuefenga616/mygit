#coding:utf-8
from sklearn.datasets import load_digits

#下载数字相关数据集
digits = load_digits()
print(digits.data.shape)    #shape表示维度1797(个特征图片)*64(个特征值)

import pylab
pylab.gray()
pylab.matshow(digits.images[0])
pylab.show()