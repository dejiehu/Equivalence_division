import math
import time
from itertools import chain
import numpy
import copy

def readfile(filename):
    my_data = numpy.loadtxt(filename)
    my_data = my_data.astype(int)
    print(my_data)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

def del_dup(U_con_data,core_list):#删除重复列
    attr_list = [i for i in range(len(U_con_data))]
    j = U_con_data.shape[1] - 1
    while j >= 0:
        if core_list.__contains__(j):
            U_con_data = deal_data(U_con_data, j, j)
            del attr_list[j]
        j -= 1
    return U_con_data,attr_list

def cal_red_divlist(red_num,con_data):   #根据核属性数值计算核属性数据
    red_data = numpy.empty(shape=(len(con_data), 0))
    red_data = red_data.astype(int)
    for i in red_num:
        red_data =  numpy.append(red_data,con_data[:,i,numpy.newaxis],axis=1)
    return red_data

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

def merge_divlist(U_data,Ux_data,U_divlist,Ux_divlist):#      U/C + Ux/C
    U_con_divlist = []
    Ux_con_divlist = []
    for i in range(len(Ux_divlist)-1,-1,-1):  #逆序循环
        for j in range(len(U_divlist)-1,-1,-1):
            if (U_data[U_divlist[j][0]] == Ux_data[(Ux_divlist[i][0]) - U_data.shape[0]]).all():
                U_con_divlist.append(U_divlist[j])
                Ux_con_divlist.append(Ux_divlist[i])
                break
    return U_con_divlist,Ux_con_divlist

def pairs_of_object(x):  #类对的个数
    return x*(x-1)/2

def CCE_Entropy(con_divlist,dec_divlist):    #组合熵
    U_list = list(chain.from_iterable(con_divlist))
    U_len = len(U_list)
    c_entropy = 0
    for i in con_divlist:
        c_entropy += (len(i)/U_len)*(pairs_of_object(len(i)) / pairs_of_object(U_len))
        for j in dec_divlist:
            Intersect_list = set(i) & set(j)
            if len(Intersect_list) != 0:
                c_entropy -= (len(Intersect_list)/U_len)*(pairs_of_object(len(Intersect_list)) / pairs_of_object(U_len))
    return c_entropy

def U_Ux_CCE_Entropy(U_con_data,U_dec_data,Ux_con_data,Ux_dec_data):
    U_con_divlist = div(U_con_data)
    U_dec_divlist = div(U_dec_data)
    Ux_con_divlist = div(Ux_con_data)
    Ux_dec_divlist = div(Ux_dec_data)
    U_len = U_con_data.shape[0]
    Ux_len = Ux_con_data.shape[0]
    Ux_con_divlist = Add_Ux_dataShape(U_len, Ux_con_divlist)
    Ux_dec_divlist = Add_Ux_dataShape(U_len, Ux_dec_divlist)
    U_comb_con_divlist,Ux_comb_con_divlist = merge_divlist(U_con_data,Ux_con_data,U_con_divlist,Ux_con_divlist)
    U_comb_dec_divlist, Ux_comb_dec_divlist = merge_divlist(U_dec_data, Ux_dec_data, U_dec_divlist,Ux_dec_divlist)
    # print( U_comb_con_divlist,Ux_comb_con_divlist)
    # print(U_comb_dec_divlist, Ux_comb_dec_divlist)
    latter = 0
    for i in range(len(U_comb_con_divlist)):
        latter += ((len(U_comb_con_divlist[i]) * len(Ux_comb_con_divlist[i])) * (3 * len(U_comb_con_divlist[i]) + 3 * len(Ux_comb_con_divlist[i]) - 2))/(math.pow(U_len + Ux_len,2) * (U_len + Ux_len - 1))
        for j in range(len(U_comb_dec_divlist)):
            latter -= (len(set(U_comb_con_divlist[i]) & set(U_comb_dec_divlist[j])) * len(set(Ux_comb_con_divlist[i]) & set(Ux_comb_dec_divlist[j])) * (3 * len(set(U_comb_con_divlist[i]) & set(U_comb_dec_divlist[j])) + 3 * len(set(Ux_comb_con_divlist[i]) & set(Ux_comb_dec_divlist[j])) - 2)) / (math.pow(U_len + Ux_len,2) * (U_len + Ux_len - 1))
    # print/(CCE_Entropy(U_con_divlist,U_dec_divlist),'')
    # print((math.pow(U_len,2) * (U_len - 1) * CCE_Entropy(U_con_divlist,U_dec_divlist) + math.pow(Ux_len,2) * (Ux_len - 1) * CCE_Entropy(Ux_con_divlist,Ux_dec_divlist))/(math.pow(U_len + Ux_len , 2) * (U_len + Ux_len - 1)) + latter,"last")
    return (math.pow(U_len,2) * (U_len - 1) * CCE_Entropy(U_con_divlist,U_dec_divlist) + math.pow(Ux_len,2) * (Ux_len - 1) * CCE_Entropy(Ux_con_divlist,Ux_dec_divlist))/(math.pow(U_len + Ux_len , 2) * (U_len + Ux_len - 1)) + latter
    # return (U_len * (U_len - 1) * CCE_Entropy(U_con_divlist,U_dec_divlist) + len(set(U_Ux_con_divlist) - set(U_Ux_dec_divlist)) * (3 * len(U_Ux_con_divlist) + 3 * len(set(U_Ux_con_divlist) & set(U_Ux_dec_divlist)) - 5))/math.pow(U_len + 1,2)

def Add_Ux_dataShape(U_len,Ux_divlist):   #  调整增加的属性的对象序号
    for i in range(len(Ux_divlist)):
        for j in range(len(Ux_divlist[i])):
            Ux_divlist[i][j] += U_len
    return Ux_divlist

def Red(red_list,U_con_data,Ux_con_data,U_dec_data,Ux_dec_data):#约简
    C_entropy = U_Ux_CCE_Entropy(U_con_data, U_dec_data, Ux_con_data, Ux_dec_data)
    U_red_data = cal_red_divlist(red_list, U_con_data)
    Ux_red_data = cal_red_divlist(red_list, Ux_con_data)
    Ux_con_divlist = Add_Ux_dataShape(U_con_data.shape[0], div(Ux_con_data))
    Ux_dec_divlist = Add_Ux_dataShape(Ux_con_data.shape[0], div(Ux_dec_data))
    U_comb_con_divlist, Ux_comb_con_divlist = merge_divlist(U_con_data, Ux_con_data, div(U_con_data), Ux_con_divlist)
    U_comb_dec_divlist, Ux_comb_dec_divlist = merge_divlist(U_dec_data, Ux_dec_data, div(U_dec_data), Ux_dec_divlist)
    red_entropy = U_Ux_CCE_Entropy(U_red_data, U_dec_data, Ux_red_data, Ux_dec_data)
    if len(U_comb_con_divlist) == 0 & len(U_comb_dec_divlist) == 0:
        if C_entropy == red_entropy:
            print(red_list,"停止")
    attr_data,attr_list = del_dup(U_con_data, red_list)
    dict = {}
    while C_entropy != red_entropy:
        dict.clear()
        con_key = -1  # 字典key
        con_value = -1  # 字典value
        for i in range(attr_data.shape[1]):
            U_temp_red_data = numpy.append(U_red_data,attr_data[:,i,numpy.newaxis],axis=1)
            Ux_temp_red_data = numpy.append(Ux_red_data, attr_data[:, i, numpy.newaxis], axis=1)
            dict[i] = U_Ux_CCE_Entropy(U_temp_red_data, U_dec_data, Ux_temp_red_data, Ux_dec_data)
        for key in dict:
            if dict[key] > con_value:
                con_value = dict[key]
                con_key = key
        U_red_data = numpy.append(U_red_data, attr_data[:, con_key, numpy.newaxis], axis=1)
        Ux_red_data = numpy.append(Ux_red_data, attr_data[:, con_key, numpy.newaxis], axis=1)
        red_entropy = U_Ux_CCE_Entropy(U_red_data, U_dec_data, Ux_red_data, Ux_dec_data)
        red_list.append(attr_data[con_key])
        del attr_data[con_key]
    De_redundancy(C_entropy, U_dec_data, Ux_dec_data, U_red_data, Ux_red_data, red_list)
    print(attr_list)
    print(red_list,"core_list")

def De_redundancy(C_entropy, U_dec_data, Ux_dec_data, U_red_data, Ux_red_data, red_list):  #去冗余
    i = 0
    while i < U_red_data.shape[1]:
        U_temp_red_data = deal_data(U_red_data, i, i)
        Ux_temp_red_data = deal_data(Ux_red_data, i, i)
        if U_Ux_CCE_Entropy(U_temp_red_data,U_dec_data,Ux_temp_red_data,Ux_dec_data) == C_entropy:
            U_red_data = deal_data(U_red_data, i, i)
            Ux_red_data = deal_data(Ux_red_data, i, i)
            del red_list[i]
            i = 0
            continue
        i += 1
    return red_list, U_red_data, Ux_red_data

if __name__ == '__main__':
    start = time.perf_counter()
    U_data = readfile("table_1.txt")
    Ux_data = readfile("add_multiple.txt")
    red_list = [0,1,3]
    U_con_data = deal_data(U_data, U_data.shape[1] - 1, U_data.shape[1] - 1)
    U_dec_data = deal_data(U_data, 0, U_data.shape[1] - 2)
    Ux_con_data = deal_data(Ux_data, Ux_data.shape[1] - 1, Ux_data.shape[1] - 1)
    Ux_dec_data = deal_data(Ux_data, 0, Ux_data.shape[1] - 2)
    Red(red_list,U_con_data,Ux_con_data,U_dec_data,Ux_dec_data)
    end = time.perf_counter()
    print(end - start)