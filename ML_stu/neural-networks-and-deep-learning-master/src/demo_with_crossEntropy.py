#coding:utf-8
import mnist_loader
import network2

training_data,validation_data,test_data = mnist_loader.load_data_wrapper()
print "training data"
print type(training_data)
print len(training_data)
print training_data[0][0].shape
print training_data[0][1].shape

print "validation data"
print len(validation_data)

print "test data"
print len(test_data)

net = network2.Network([784, 30, 10], cost=network2.CrossEntropyCost)      # 784个特征，隐藏层30个，输出层10个
# net.large_weight_initializer()  #专门标记一下，是因为之后我们会用其他方法来初始化
net.SGD(training_data, 30, 10, 0.5, evaluation_data=test_data, monitor_evaluation_accuracy=True)    # 30轮，mini_batch 10个，学习率0.5
