#coding:utf-8
import math

def euclideanDistance(x1,y1,x2,y2):
    d = math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2))
    return d

d_ag = euclideanDistance(3,104,18,90)
d_bg = euclideanDistance(2,100,18,90)
d_cg = euclideanDistance(1,81,18,90)
d_dg = euclideanDistance(101,100,18,90)
d_eg = euclideanDistance(99,5,18,90)
d_fg = euclideanDistance(98,2,18,90)


print("d_ag: ", d_ag)
print("d_bg: ", d_bg)
print("d_cg: ", d_cg)
print("d_dg: ", d_dg)
print("d_eg: ", d_eg)
print("d_fg: ", d_fg)