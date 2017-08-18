#coding:utf-8
import csv
import random
import math
import operator

def loadDataset(filename, split, trainingSet=[], testSet=[]):   #数据集分成两部分：训练集、测试集
    with open(filename,'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)-1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:     # random.random() < 1
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])

def enclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):     #算出空间距离
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):  #计算样本集的元素 与 测试集元素 的距离，取k个
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = enclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))  #按xx排序，从小到大
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])   #得到k个邻居
    return neighbors

def getResponse(neighbors):     #根据投票法则归类
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)  #从大到小
    return sortedVotes[0][0]    #得到第一个投票分类

def getAccuracy(testSet, predictions):  #预测成功率
    correct = 0     #猜对的个数
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:    #testSet[x][-1]是实际归类
            correct += 1
    return (correct/float(len(testSet))) * 100.0    #百分比取值

if __name__ == '__main__':
    trainingSet = []
    testSet = []
    split = 0.67
    loadDataset("./irisdata.txt", split, trainingSet, testSet)      #数据集有150行
    print("train set :" + repr(len(trainingSet)))
    print("test set :" + repr(len(testSet)))

    predictions = []
    k = 3   #取3个邻居
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print("predcted =" + repr(result) + ", actual=" + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print("accuracy:" + str(accuracy) + "%")