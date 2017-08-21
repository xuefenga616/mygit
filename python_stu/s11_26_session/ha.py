#!/usr/bin/env python
#coding:utf-8

import sys
import math
from bisect import bisect


if sys.version_info >= (2, 5):
    import hashlib
    md5_constructor = hashlib.md5
else:
    import md5
    md5_constructor = md5.new


class HashRing(object):
    """一致性哈希"""

    def __init__(self,nodes):
        '''初始化
        nodes : 初始化的节点，其中包含节点已经节点对应的权重
                默认每一个节点有32个虚拟节点
                对于权重，通过多创建虚拟节点来实现
                如：nodes = [
                        {'host':'127.0.0.1:8000','weight':1},
                        {'host':'127.0.0.1:8001','weight':2},
                        {'host':'127.0.0.1:8002','weight':1},
                    ]
        '''

        self.ring = dict()
        self._sorted_keys = []

        self.total_weight = 0

        self.__generate_circle(nodes)



    def __generate_circle(self,nodes):
        for node_info in nodes:
            self.total_weight += node_info.get('weight',1)

        for node_info in nodes:
            weight = node_info.get('weight',1)
            node = node_info.get('host',None)

            virtual_node_count = math.floor((32*len(nodes)*weight) / self.total_weight)
            for i in xrange(0,int(virtual_node_count)):
                key = self.gen_key_thirty_two( '%s-%s' % (node, i) )
                if self._sorted_keys.__contains__(key):
                    raise Exception('该节点已经存在.')
                self.ring[key] = node
                self._sorted_keys.append(key)

    def add_node(self,node):
        ''' 新建节点
        node : 要添加的节点，格式为：{'host':'127.0.0.1:8002','weight':1}，其中第一个元素表示节点，第二个元素表示该节点的权重。
        '''
        node = node.get('host',None)
        if not node:
                raise Exception('节点的地址不能为空.')

        weight = node.get('weight',1)

        self.total_weight += weight
        nodes_count = len(self._sorted_keys) + 1

        virtual_node_count = math.floor((32 * nodes_count * weight) / self.total_weight)
        for i in xrange(0,int(virtual_node_count)):
            key = self.gen_key_thirty_two( '%s-%s' % (node, i) )
            if self._sorted_keys.__contains__(key):
                raise Exception('该节点已经存在.')
            self.ring[key] = node
            self._sorted_keys.append(key)

    def remove_node(self,node):
        ''' 移除节点
        node : 要移除的节点 '127.0.0.1:8000'
        '''
        for key,value in self.ring.items():
            if value == node:
                del self.ring[key]
                self._sorted_keys.remove(key)

    def get_node(self,string_key):
        '''获取 string_key 所在的节点'''
        pos = self.get_node_pos(string_key)
        if pos is None:
            return None
        return self.ring[ self._sorted_keys[pos]].split(':')

    def get_node_pos(self,string_key):
        '''获取 string_key 所在的节点的索引'''
        if not self.ring:
            return None

        key = self.gen_key_thirty_two(string_key)
        nodes = self._sorted_keys
        pos = bisect(nodes, key)
        return pos

    def gen_key_thirty_two(self, key):

        m = md5_constructor()
        m.update(key)
        return long(m.hexdigest(), 16)

    def gen_key_sixteen(self,key):

        b_key = self.__hash_digest(key)
        return self.__hash_val(b_key, lambda x: x)

    def __hash_val(self, b_key, entry_fn):
        return (( b_key[entry_fn(3)] << 24)|(b_key[entry_fn(2)] << 16)|(b_key[entry_fn(1)] << 8)| b_key[entry_fn(0)] )

    def __hash_digest(self, key):
        m = md5_constructor()
        m.update(key)
        return map(ord, m.digest())



nodes = [
    {'host':'127.0.0.1:8000','weight':1},
    {'host':'127.0.0.1:8001','weight':2},
    {'host':'127.0.0.1:8002','weight':1},
]

ring = HashRing(nodes)
result = ring.get_node('98708798709870987098709879087')
print result

