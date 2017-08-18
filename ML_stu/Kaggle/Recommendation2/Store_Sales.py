#coding:utf-8
import pandas as pd
import datetime
import csv
import numpy as np
import os
import scipy
import xgboost as xgb
import itertools
import operator
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.base import TransformerMixin
from sklearn import cross_validation
from matplotlib import pylab,pyplot
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

goal = "Sales"
myid = "Id"

def train_preprocess():
    pass