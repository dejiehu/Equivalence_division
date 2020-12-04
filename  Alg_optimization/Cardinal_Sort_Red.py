import operator
import time
from itertools import chain

import numpy

def readfile():
    my_data = numpy.loadtxt('../german.txt')
    my_data = my_data.astype(int)
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
    print(Mm_list)
    U_linkList = [i for i in range(len(my_data))]
    for i in range(len(Mm_list)):
        queue_linkList = [[]]*(Mm_list[i][0] - Mm_list[i][1] + 1)
        for j in U_linkList:
            queue_linkList[my_data[j][i] - Mm_list[i][1]] = queue_linkList[my_data[j][i] - Mm_list[i][1]] + [j]
        U_linkList.clear()
        U_linkList = list(chain.from_iterable(queue_linkList))
    print(U_linkList)
    div_list = []
    temp_list = [U_linkList[0]]
    for i in range(1,len(U_linkList)):
        print((my_data[U_linkList[i]] == my_data[U_linkList[i-1]]).all(),U_linkList[i]+1,my_data[U_linkList[i]] ,U_linkList[i-1]+1, my_data[U_linkList[i-1]])
        if((my_data[U_linkList[i]] == my_data[U_linkList[i-1]]).all()):
            temp_list.append(U_linkList[i])
            continue
        div_list.append(temp_list)
        temp_list = [U_linkList[i]]
    div_list.append(temp_list)
    print(div_list)
    return U_linkList








if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile()
    # con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    # dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    Mm_list = Max_min(my_data)
    div(my_data, Mm_list)
    end = time.perf_counter()
    print(end - start)