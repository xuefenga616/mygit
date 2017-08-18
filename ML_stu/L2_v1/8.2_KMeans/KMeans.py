#coding:utf-8
import numpy

def kmeans(X, k, maxIt):    # maxIt是迭代次数
    numPoints, numDim = X.shape

    dataSet = numpy.zeros((numPoints, numDim+1))    # 填充矩阵，加一列拿来归类
    dataSet[:, :-1] = X

    # init centroids randomly   找k个随机点
    centroids = dataSet[numpy.random.randint(numPoints, size=k), :]     #从numPoints行中随机选择k行，后面：表示所有列

    centroids[:, -1] = range(1, k+1)    #最后1列初始化1个值：1 ~ k

    #init book keeping vars
    iterations = 0
    oldCentroids = None

    # run the main k-means algorithm    旧的中心点与新的中心点不相等，则不停止
    while not shouldStop(oldCentroids, centroids, iterations, maxIt):
        print("iteration:\n", iterations)
        print("dataSet:\n", dataSet)
        print("centroids:\n", centroids)

        #save old centroids for convergence test, book keeping
        oldCentroids = numpy.copy(centroids)    #深拷贝
        iterations += 1

        #assign labels to each datapoint based on centroids
        updateLabels(dataSet, centroids)        #重新归类

        #assign centroids based on datapoint labels
        centroids = getCentroids(dataSet, k)    #得到新的中心点

    return dataSet

def shouldStop(oldCentroids, centroids, iterations, maxIt):
    if iterations > maxIt:
        return True
    return numpy.array_equal(oldCentroids,centroids)

def updateLabels(dataSet, centroids):       #重新归类
    numPoints,numDim = dataSet.shape
    for i in range(numPoints):
        dataSet[i, -1] = getLabelFromClosestCentroid(dataSet[i,:-1],centroids)

def getLabelFromClosestCentroid(dataSetRow,centroids):
    label = centroids[0, -1]        # 初始化label为第一个中心点的值
    minDist = numpy.linalg.norm(dataSetRow - centroids[0, :-1]) #两个向量的距离
    for i in range(1, centroids.shape[0]):
        dist = numpy.linalg.norm(dataSetRow - centroids[i, :-1])
        if dist < minDist:
            minDist = dist      # 得到最小值
            label = centroids[i, -1]
    print("minDist: ", minDist)
    return label                # label即是每个点的重新归类

def getCentroids(dataSet, k):
    result = numpy.zeros((k,dataSet.shape[1]))
    for i in range(1, k+1):
        oneCluster = dataSet[dataSet[:, -1] == i, :-1]      # 1类
        result[i-1, :-1] = numpy.mean(oneCluster, axis=0)   # 求平均值，axis=0表示对行求平均值
        result[i-1, -1] = i
    return result


x1 = numpy.array([1,1])
x2 = numpy.array([2,1])
x3 = numpy.array([4,3])
x4 = numpy.array([5,4])
testX = numpy.vstack((x1,x2,x3,x4))

result = kmeans(testX, 2, 10)
print("final result:")
print(result)