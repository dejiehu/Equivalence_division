import time
from itertools import chain
import numpy

def readfile():     #读文件
    my_data = numpy.loadtxt('../cardinal.txt')
    my_data = my_data.astype(int)
    print(my_data)
    return my_data

def deal_data(my_data, m, n):  # 处理数据表  找出条件属性和决策属性用
    if n + 1 > m:
        for d in range(n, m - 1, -1):
            my_data = numpy.delete(my_data, d, 1)  # d为下标
    return my_data

def Max_min(con_data,U_list):  #找出属性最大最小值
    Mm_list = []
    for i in range(con_data.shape[1]):
        min = 10000
        Max = 0
        for j in U_list:
            if con_data[j][i] > Max:
                Max = con_data[j][i]
            if con_data[j][i] < min:
                min = con_data[j][i]
        Mm_list.append([Max,min])
    return Mm_list

def div(my_data,U_list):    #等价类的划分
    Mm_list = Max_min(my_data,U_list)
    for i in range(len(Mm_list)):
        queue_linkList = [[]]*(Mm_list[i][0] - Mm_list[i][1] + 1)
        for j in U_linkList:
            queue_linkList[my_data[j][i] - Mm_list[i][1]] = queue_linkList[my_data[j][i] - Mm_list[i][1]] + [j]
        U_linkList.clear()
        U_linkList = list(chain.from_iterable(queue_linkList))
    div_list = []
    temp_list = [U_linkList[0]]
    for i in range(1,len(U_linkList)):
        if((my_data[U_linkList[i]] == my_data[U_linkList[i-1]]).all()):
            temp_list.append(U_linkList[i])
            continue
        div_list.append(temp_list)
        temp_list = [U_linkList[i]]
    div_list.append(temp_list)
    return div_list

def Reduce_basedSig(my_data):
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    U_list = [i for i in range(len(my_data))]
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    Max_min(con_data, U_list)
    # con_list = div(con_data, Max_min(con_data,U_list),U_list)      #U/C

if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile()
    Reduce_basedSig(my_data)
    end = time.perf_counter()
    print(end - start)