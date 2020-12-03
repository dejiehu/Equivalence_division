import time
import numpy

def readfile():
    my_data = numpy.loadtxt('../data.txt')
    print(my_data)
    return my_data

def deal_data(my_data, m, n):  # 处理数据表
    if n + 1 > m:
        for d in range(n, m - 1, -1):
            my_data = numpy.delete(my_data, d, 1)  # d为下标
    return my_data

def Max_min(con_data):#找出最大最小值
    Mm_list = []
    for i in range(con_data.shape[1]):
        Mm_list.append([numpy.max(con_data[:, i]),numpy.min(con_data[:, i])])
    return Mm_list

class Node(object):
    def __init__(self, data):
        self.data = data
        self._next = None

def div(my_data,Mm_list):
    U_linkList = [i for i in range(len(my_data))]
    for i in Mm_list:








if __name__ == '__main__':
    my_data = readfile()
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    Mm_list = Max_min(con_data)
    div(my_data, Mm_list)