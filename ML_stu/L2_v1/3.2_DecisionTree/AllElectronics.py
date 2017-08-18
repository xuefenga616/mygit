#coding:utf-8
from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import preprocessing
from sklearn import tree
from sklearn.externals.six import StringIO

# dot -Tpdf ./play.dot -o play_output.pdf   # 生成决策树

rf = open("./play.csv","rb")
reader = csv.reader(rf)
headers = reader.next()
# print headers

featureList = []    #存特征
labelList = []      #存结果

for row in reader:
    labelList.append(row[len(row) - 1])
    rowDict = {}
    for i in range(1,len(row)-1):
        rowDict[headers[i]] = row[i]
    featureList.append(rowDict)
rf.close()
# print(featureList)
# print labelList

vec = DictVectorizer()
dummyX = vec.fit_transform(featureList).toarray()   #转换成0、1
# print("dummyX: " + str(dummyX))
# print(vec.get_feature_names())

lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)     #把所有列（类）转换成0、1
# print("dummyY: " + str(dummyY))

clf = tree.DecisionTreeClassifier(criterion="entropy")  #entropy信息熵
clf = clf.fit(dummyX,dummyY)
print("clf: " + str(clf))

with open("./play.dot","w") as wf:
    wf = tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file=wf)  #返回到以前的名字


# 添加一个人测试
oneRowX = dummyX[0, :]
print("oneRowX: " + str(oneRowX))

newRowX = oneRowX
newRowX[0] = 1
newRowX[2] = 0
print("newRowX: " + str(newRowX))

print(dir(clf))
predictedY = clf.predict(newRowX)
print("predictedY: " + str(predictedY))     #结果