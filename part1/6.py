import math
import time
from itertools import chain

import numpy

def readfile():
    my_data = numpy.loadtxt('../zoo.txt')
    my_data = my_data.astype(int)
    print(my_data)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

def del_dup(con_data,core_data):#删除重复列
    i = 0
    while i < core_data.shape[1]:
        j = 0
        while j < con_data.shape[1]:
            if (core_data[:, i] == con_data[:, j]).all():
                con_data = deal_data(con_data, j, j)
                continue
            j += 1
        i += 1
    return con_data


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

def div(my_data):    #等价类的划分
    U_linkList = [i for i in range(len(my_data))]
    Mm_list = Max_min(my_data,U_linkList)
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
def Entropy(attr_divlist,j):#信息熵
    entropy = 0
    for i in attr_divlist:
        p = len(i)/len(j)
        entropy -= p*math.log(p)
    return entropy

def con_Entropy(con_divlist,dec_divlist):  #条件熵
    U_num = len(sum(dec_divlist,[]))
    con_entropy = 0
    for j in con_divlist:
        s = list()
        for k in dec_divlist:
            if len((set(j) & set(k))) != 0:
                s.append(list(set(j) & set(k)))
        con_entropy += ((len(j)/U_num) * Entropy(s,j))
    return con_entropy

def core(con_data, dec_divlist,con_entropy):  #基于条件熵求核
    core_data = numpy.empty(shape=(con_data.shape[0],0))
    core_data = core_data.astype(int)
    for i in range(con_data.shape[1]):
        temp_con_data = deal_data(con_data,i,i)
        temp_con_divlist = div(temp_con_data)
        if con_entropy != (con_Entropy(temp_con_divlist, dec_divlist)):
            print("核属性是第",i,"个")
            core_data = numpy.append(core_data, con_data[:, i,numpy.newaxis], axis=1)
    return core_data


def Red(C0_data,dec_divlist,con_entropy,attr_data):#约简
    if C0_data.size == 0:
        return "无约简"
    B = C0_data
    dict = {}
    if con_Entropy(div(C0_data),dec_divlist) == con_entropy:
        print("约简为",C0_data)
    else:
        B_entropy = -1
        num = 0
        while con_entropy != B_entropy:
            dict.clear()
            con_key = -1  # 字典key
            con_value = 10000000  # 字典value
            for i in range(attr_data.shape[1]):
                temp_C0_data = B
                temp_C0_data = numpy.append(temp_C0_data,attr_data[:,i,numpy.newaxis],axis=1)
                dict[i] = con_Entropy(div(temp_C0_data),dec_divlist);
            for key in dict:
                if dict[key] < con_value:
                    con_value = dict[key]
                    con_key = key
            B = numpy.append(B,attr_data[:,con_key,numpy.newaxis],axis=1)
            B_entropy =con_Entropy(div(B),dec_divlist);
            attr_data = deal_data(attr_data,con_key,con_key)
    return  B

def print_red(my_data,Red_data):
    red_set =[]
    for i in range(Red_data.shape[1]):
        for j in range( my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    print(red_set)

if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile()
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist",con_divlist)
    print("dec_divlist", dec_divlist)
    con_entropy = con_Entropy(con_divlist,dec_divlist)
    print("条件熵：",con_entropy)
    C0_data = core(con_data, dec_divlist,con_entropy)
    attr_data = del_dup(con_data,C0_data) #C-C0
    print_red(my_data, Red(C0_data,dec_divlist,con_entropy,attr_data))
    end = time.perf_counter()
    print(end - start)