#coding:utf-8
import random,time

def bubble_sort(array):
    for i in range(len(array)):
        for j in range(len(array)-1-i):
            if array[j] > array[j+1]:
                tmp = array[j]
                array[j] = array[j+1]
                array[j+1] = tmp
    # print array
    return array

if __name__ == '__main__':
    array = []
    pre_time = time.time()
    for i in range(10000):
        array.append(random.randrange(1000))    #生成50个小于1000的随机数
    bubble_sort(array)
    cur_time = time.time()

    print cur_time - pre_time


