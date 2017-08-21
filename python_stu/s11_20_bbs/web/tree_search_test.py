#coding:utf-8
__author__ = 'xuefeng'

data = [('',''),]
data_dic = {}

def tree_search(data_dic,parent,son):
    for k,v_dic in data_dic.items():
        if k == parent:     #find your parent
            data_dic[k][son] = {}
            print "find parent of:",son
            return
        else:
            #might in the deeper layer
            print "going to further layer..."
            tree_search(data_dic[k],parent,son) #递归查找下层

for item in data:
    parent,son = item
    if parent is None:  #has no parent
        data_dic[son] = {}
    else:   #looking for its parent
        tree_search(data_dic,parent,son)

for k,v in data_dic.items():
    print k,v


