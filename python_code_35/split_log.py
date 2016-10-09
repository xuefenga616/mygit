#coding:utf-8
__author__ = 'Administrator'

def split(filname,size):
    with open(filname,'rb') as f:
        i = 0   #计算文件切割数
        n = 0   #计算大小
        temp = open(filname+'.part'+str(i),'wb')
        buf = f.read(1024)
        while True:
            temp.write(buf)
            buf = f.read(1024)
            if not buf:
                print(filname+'.part'+str(i))
                temp.close()
                return
            n += 1
            if n == size:
                n = 0
                print(filname+'.part'+str(i))
                i += 1
                temp.close()
                temp = open(filname+'.part'+str(i),'wb')

if __name__ == '__main__':
    #name = input('input filename:')
    #size = int(input('Please input size(M):'))  #输入分割后的大小，以M为单位
    name = 'D:\\spider\\bj.txt'
    size = 1
    split(name,1024*size)