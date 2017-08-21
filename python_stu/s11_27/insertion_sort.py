#coding:utf-8
import random,time

def insertion_sort(array):
    for i in range(1,len(array)):
        pos = i     #刚开始的位置
        cur_val = array[i]
        while pos > 0 and cur_val < array[pos-1]:
            array[pos] = array[pos-1]
            pos -= 1
        array[pos] = cur_val


    # print array
    return array

if __name__ == '__main__':
    array = []
    pre_time = time.time()
    for i in range(10000):
        array.append(random.randrange(1000))    #生成50个小于1000的随机数
    insertion_sort(array)
    cur_time = time.time()

    print cur_time - pre_time

