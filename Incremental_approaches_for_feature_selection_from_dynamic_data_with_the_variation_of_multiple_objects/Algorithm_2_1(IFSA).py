import math
import time
from itertools import chain
import numpy
'''
《多目标变化下动态数据特征选择的增量方法》
基于依赖度的增量式属性约简   添加
'''

def readfile(file):     #读文件
    my_data = numpy.loadtxt(file)
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

def div_object(my_data,U_linkList):    #按照指定对象等价类的划分
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

def Positive_reign(con_data,dec_data): #正域
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    pos_list = []
    for i in dec_divlist:
        for j in con_divlist:
            if set(j).issubset(i):
                pos_list += j
    return len(pos_list)

def U_Ux_dependency(U_dec_data,Ux_dec_data,U_con_data,Ux_con_data):#计算新的依赖度函数
    return (Positive_reign(U_con_data,U_dec_data) + Positive_reign(Ux_con_data,Ux_dec_data) -
            merge_divlist(U_con_data,Ux_con_data,U_dec_data,Ux_dec_data))/(U_con_data.shape[0] + Ux_con_data.shape[0])

def red(U_dec_data, U_con_data,Ux_dec_data,Ux_con_data,RED):# 求约简
    U_red_data = cal_red_divlist(RED, U_con_data)
    Ux_red_data = cal_red_divlist(RED, Ux_con_data)
    U_Ux_C_dep = U_Ux_dependency(U_dec_data,Ux_dec_data,U_con_data,Ux_con_data)
    if U_Ux_C_dep  == U_Ux_dependency(U_dec_data,Ux_dec_data,U_red_data,Ux_red_data):
        print("去冗余了")
        RED, U_red_data, Ux_red_data = De_redundancy(U_Ux_C_dep, U_dec_data, Ux_dec_data, U_red_data, Ux_red_data, RED)
        return RED, U_red_data, Ux_red_data
    attr_num = []
    for i in range(U_con_data.shape[1]):
        if not (RED.__contains__(i)):
            attr_num += [i]
    U_attr_data = cal_red_divlist(attr_num,U_con_data)
    Ux_attr_data = cal_red_divlist(attr_num,Ux_con_data)
    dict = {}
    U_Ux_red_dep = U_Ux_dependency(U_dec_data, Ux_dec_data, U_red_data, Ux_red_data)
    for i in range(U_attr_data.shape[1]):
        U_temp_red_data = U_red_data
        Ux_temp_red_data = Ux_red_data
        U_temp_red_data = numpy.append(U_temp_red_data, U_attr_data[:, i, numpy.newaxis], axis=1)
        Ux_temp_red_data = numpy.append(Ux_temp_red_data, Ux_attr_data[:, i, numpy.newaxis], axis=1)
        dict[i] = U_Ux_dependency(U_dec_data,Ux_dec_data,U_temp_red_data,Ux_temp_red_data) - U_Ux_red_dep
    dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    # print(dict)
    while U_Ux_dependency(U_dec_data,Ux_dec_data,U_red_data,Ux_red_data) != U_Ux_C_dep:
        print(dict,dict[0])
        print(attr_num)
        U_red_data = numpy.append(U_red_data, U_attr_data[:, dict[0][0], numpy.newaxis], axis=1)
        Ux_red_data = numpy.append(Ux_red_data, Ux_attr_data[:, dict[0][0], numpy.newaxis], axis=1)
        RED += [attr_num[dict[0][0]]]
        del dict[0]
    RED,U_red_data,Ux_red_data = De_redundancy(U_Ux_C_dep, U_dec_data, Ux_dec_data, U_red_data, Ux_red_data, RED)
    print(RED)
    return RED,U_red_data,Ux_red_data

def De_redundancy(U_Ux_C_dep,U_dec_data, Ux_dec_data,U_red_data,Ux_red_data,RED):# 去冗余
    i = 0
    while i < U_red_data.shape[1]:
        U_temp_red_data = U_red_data
        Ux_temp_red_data = Ux_red_data
        U_temp_red_data = deal_data(U_temp_red_data,i,i)
        Ux_temp_red_data = deal_data(Ux_temp_red_data, i, i)
        if U_Ux_dependency(U_dec_data,Ux_dec_data,U_temp_red_data,Ux_temp_red_data) == U_Ux_C_dep:
            U_red_data = deal_data(U_red_data,i,i)
            Ux_red_data = deal_data(Ux_red_data, i, i)
            del RED[i]
            i = 0
            continue
        i += 1
    return RED,U_red_data,Ux_red_data

def Add_Ux_dataShape(U_data,Ux_divlist):   #  调整增加的属性的对象序号
    for i in range(len(Ux_divlist)):
        for j in range(len(Ux_divlist[i])):
            Ux_divlist[i][j] += U_data.shape[0]
    return Ux_divlist

def cal_red_divlist(red_num,con_data):   #根据核属性数值计算核属性数据
    red_data = numpy.empty(shape=(len(con_data), 0))
    red_data = red_data.astype(int)
    for i in red_num:
        red_data =  numpy.append(red_data,con_data[:,i,numpy.newaxis],axis=1)
    return red_data

def merge_divlist(U_data,Ux_data,U_dec,Ux_dec):#      U/C + Ux/C
    U_divlist = div(U_data)
    Ux_divlist = div(Ux_data)
    Ux_divlist = Add_Ux_dataShape(U_data, Ux_divlist)
    U_Ux_divlist = []
    sum = 0
    for i in range(len(Ux_divlist)-1,-1,-1):  #逆序循环
        for j in range(len(U_divlist)-1,-1,-1):
            if (U_data[U_divlist[j][0]] == Ux_data[(Ux_divlist[i][0]) - U_data.shape[0]]).all():
                U_Ux_divlist.append(U_divlist[j] + Ux_divlist[i])
                del U_divlist[j],Ux_divlist[i]
                break
    # for i in U_Ux_divlist:
    #     Xi = len(div_object(numpy.append(U_dec,Ux_dec,axis=0),i))
    #     if Xi != 1:
    #         sum += Xi
    for i in U_Ux_divlist:
        if len(div_object(numpy.append(U_dec, Ux_dec, axis=0), i)) != 1:
            sum += len(i)
    return sum

if __name__ == '__main__':
    start = time.perf_counter()
    U_data = readfile('table_1.txt')
    RED = [0, 3]
    Ux_data = readfile('incremental.txt')
    U_Ux_data = numpy.append(U_data,Ux_data,axis=0)

    U_con_data = deal_data(U_data, U_data.shape[1] - 1, U_data.shape[1] - 1)
    U_dec_data = deal_data(U_data, 0, U_data.shape[1] - 2)

    Ux_con_data = deal_data(Ux_data, Ux_data.shape[1] - 1, Ux_data.shape[1] - 1)
    Ux_dec_data = deal_data(Ux_data, 0, Ux_data.shape[1] - 2)

    red(U_dec_data, U_con_data, Ux_dec_data, Ux_con_data,RED)
    end = time.perf_counter()
    print(end - start)