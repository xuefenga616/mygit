#coding:utf-8
import numpy        #矩阵

def tanh(x):        #双曲正切（-1，1）
    return numpy.tanh(x)

def tanh_deriv(x):  #求导数：一个函数在某一点的倒数描述了这个函数在这一点附近的变化率
    return 1.0 - numpy.tanh(x)*numpy.tanh(x)

def logistic(x):    #逻辑函数（0，1）
    return 1 / (1 + numpy.exp(-x))

def logistic_deriv(x):
    return logistic(x) * (1 - logistic(x))

class NeuralNetwork(object):
    def __init__(self, layers, active="tanh"):      #layers是指每层里有多少个神经元
        if active == "logistic":
            self.active = logistic
            self.active_deriv = logistic_deriv
        elif active == "tanh":
            self.active = tanh
            self.active_deriv = tanh_deriv

        self.weights = []       #权重集合
        for i in range(1, len(layers)-1):   #遍历隐藏层-0.25到0.25
            self.weights.append((2 * numpy.random.random((layers[i - 1] + 1, layers[i] + 1)) - 1) * 0.25)   #从i-1到i
            self.weights.append((2 * numpy.random.random((layers[i] + 1, layers[i + 1])) - 1) * 0.25)       #从i到i+1

    def fit(self, X, y, learning_rate=0.2, epochs=10000):   #X对应一个实例，learning_rate学习率，epochs抽样循环次数
        X = numpy.atleast_2d(X)     #数据类型改为numpy，至少2维，比如：10*100
        temp = numpy.ones([X.shape[0], X.shape[1]+1])   #初始化全是1的矩阵，X.shape[0]=10，X.shape[1]=100，多1列
        temp[:, 0:-1] = X   # adding the bias unit to the input layer
        X = temp
        y = numpy.array(y)  #分类标记

        for k in range(epochs):
            # 先随机选一个X实例
            i = numpy.random.randint(X.shape[0])
            a = [X[i]]

            for l in range(len(self.weights)):
                a.append(self.active(numpy.dot(a[l], self.weights[l])))     #内积：值*权重，再tanh()
            error = y[i] - a[-1]                #误差
            deltas = [error * self.active_deriv(a[-1])]     #更新过后的误差（最后的）

            for l in range(len(a)-2, 0, -1):    #倒序
                deltas.append(deltas[-1].dot(self.weights[l].T) * self.active_deriv(a[l]))
            deltas.reverse()        #反转一下
            for i in range(len(self.weights)):
                layer = numpy.atleast_2d(a[i])
                delta = numpy.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)   #更新权重

    def predict(self, x):
        x = numpy.array(x)
        temp = numpy.ones(x.shape[0] + 1)
        temp[0:-1] = x
        a = temp
        for l in range(len(self.weights)):
            a = self.active(numpy.dot(a, self.weights[l]))
        return a    #取最后值
    

