#coding:utf-8
import random,time

def select_sort(array):
    for i in range(len(array)):
        s_index = i
        for j in range(i,len(array)):
            if array[s_index] > array[j]:
                s_index = j
        tmp = array[i]
        array[i] = array[s_index]
        array[s_index] = tmp

    # print array
    return array

if __name__ == '__main__':
    array = []
    pre_time = time.time()
    for i in range(10000):
        array.append(random.randrange(1000))    #生成50个小于1000的随机数
    select_sort(array)
    cur_time = time.time()

    print cur_time - pre_time

