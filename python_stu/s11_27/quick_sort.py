#coding:utf-8
import random,time

def quick_sort(array,start,end):
    if start >= end:
        return
    k = array[start]
    left_flag = start        #左边的小旗子
    right_flag = end         #右边的小旗子

    while left_flag < right_flag:
        while left_flag < right_flag and array[right_flag] > k:    #代表要往左边移动小旗子
            right_flag -= 1
        tmp = array[right_flag]
        array[right_flag] = array[left_flag]
        array[left_flag] = tmp

        while left_flag < right_flag and array[left_flag] <= k:
            left_flag += 1
        tmp = array[right_flag]
        array[right_flag] = array[left_flag]
        array[left_flag] = tmp

    quick_sort(array,start,left_flag-1)
    quick_sort(array,left_flag+1,end)

    return array

if __name__ == '__main__':
    array = []
    pre_time = time.time()
    for i in range(10000):
        array.append(random.randrange(1000))    #生成50个小于1000的随机数
    # print len(array)
    quick_sort(array,0,len(array)-1)
    cur_time = time.time()

    print cur_time - pre_time

