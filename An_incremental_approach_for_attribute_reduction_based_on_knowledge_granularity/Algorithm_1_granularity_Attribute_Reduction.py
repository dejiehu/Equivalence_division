import math
from itertools import chain
import numpy
'''
基于知识粒的属性约简
'''

def readfile():     #读文件
    my_data = numpy.loadtxt('table_1.txt')
    my_data = my_data.astype(int)
    print(my_data)
    print("*******************************************************************")
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

def granularity(con_divlist): #知识粒
    GP = 0
    U = len(list(chain.from_iterable(con_divlist)))
    for i in con_divlist:
        GP = math.pow(len(i),2)/math.pow(U,2) +GP
    return GP

def condition_granularity(dec_data,con_data):  #相对条件粒计算
    return granularity(div(con_data)) - granularity(div(numpy.append(con_data,dec_data,axis=1)))

def Core(dec_data,con_data):  #求核
    core_data = numpy.empty(shape=(len(con_data), 0))
    core_data = core_data.astype(int)
    core = []
    for i in range(con_data.shape[1]):
        temp_core_data = deal_data(con_data,i,i)
        if condition_granularity(dec_data,temp_core_data) - condition_granularity(dec_data,con_data) != 0:
            core_data = numpy.append(core_data, con_data[:, i, numpy.newaxis], axis=1)
            core += [i]
    print(core)
    return core_data,core

def red(dec_data, con_data):# 求约简
    red_data,red_num = Core(dec_data,con_data)
    if len(red_num) == 0:
        print("无约简")
        return
    attr_data = numpy.empty(shape=(len(con_data), 0))
    attr_data = attr_data.astype(int)
    attr_num = []
    for i in range(con_data.shape[1]):
        if not(red_num.__contains__(i)):
            attr_data = numpy.append(attr_data, con_data[:, i, numpy.newaxis], axis=1)
            attr_num += [i]
    print(condition_granularity(dec_data,con_data),"gpu")
    while condition_granularity(dec_data,con_data) != condition_granularity(dec_data,red_data):
        dict = {}
        con_key = -1  # 字典key
        con_value = -1  # 字典value
        for i in range(attr_data.shape[1]):
            temp_red_data = red_data
            temp_red_data = numpy.append(temp_red_data, attr_data[:, i, numpy.newaxis], axis=1)
            dict[i] = condition_granularity(dec_data,red_data) - condition_granularity(dec_data,temp_red_data)
        print(dict)
        for key in dict:
            if dict[key] > con_value:
                con_value = dict[key]
                con_key = key
        red_data = numpy.append(red_data,attr_data[:,con_key,numpy.newaxis],axis=1)
        red_num += [attr_num[con_key]]
        attr_data = deal_data(attr_data, con_key, con_key)
        del attr_num[con_key]
    return red_data,red_num

def De_redundancy(red_data,red_num,dec_data,con_data):# 去冗余
    i = 0
    while i < red_data.shape[1]:
        temp_Red_data = red_data
        temp_Red_data = deal_data(temp_Red_data,i,i)
        if condition_granularity(dec_data,con_data) == condition_granularity(dec_data,temp_Red_data):
            red_data = deal_data(red_data,i,i)
            del red_num[i]
            i = 0
            continue
        i += 1
    print(red_data)
    print(red_num)
    return red_data,red_num

if __name__ == '__main__':
    my_data = readfile()
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    red_data,red_num = red(dec_data, con_data)
    red_data,red_num = De_redundancy(red_data, red_num, dec_data, con_data)
