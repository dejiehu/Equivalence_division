import math
import time
from itertools import chain
import numpy

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
    Mm_list = Max_min(my_data,U_linkList)     #最大值最小值列表
    for i in range(len(Mm_list)):
        queue_linkList = [[]]*(Mm_list[i][0] - Mm_list[i][1] + 1)    #queue_linkList 链表
        for j in U_linkList:
            queue_linkList[my_data[j][i] - Mm_list[i][1]] = queue_linkList[my_data[j][i] - Mm_list[i][1]] + [j]
        U_linkList.clear()
        U_linkList = list(chain.from_iterable(queue_linkList))   #二维数组变一维
    div_list = []
    temp_list = [U_linkList[0]]    #U_linkList为对最后属性划分完的结果（链表）
    for i in range(1,len(U_linkList)):     #   将最后的链表变成划分的集合
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

def SCE_Entropy(U_con_divlist,U_dec_divlist):  #香农条件熵
    U_num = len(sum(U_dec_divlist, []))
    con_entropy = 0
    for j in U_con_divlist:
        s = list()
        for k in U_dec_divlist:
            if len((set(j) & set(k))) != 0:
                s.append(list(set(j) & set(k)))
        con_entropy += ((len(j)/U_num) * Entropy(s,j))
    return con_entropy

def LCE_Entropy(con_divlist,dec_divlist):  #梁的熵
    U_list = list(chain.from_iterable(con_divlist))
    U_len = len(U_list)
    l_entropy = 0
    for i in con_divlist:
        for j in dec_divlist:
            i_c = (set(U_list).difference(set(i)))   #补集
            j_c = (set(U_list).difference(set(j)))   #补集
            if (len((set(i) & set(j))) != 0) & (len(i_c & j_c) != 0):
                l_entropy += (((len((set(i) & set(j)))/U_len) * (len(i_c & j_c))/U_len))
    return l_entropy

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

def core(U_con_data, U_dec_divlist,con_entropy):  #基于条件熵求核
    core_list = []
    core_data = numpy.empty(shape=(U_con_data.shape[0],0))
    core_data = core_data.astype(int)
    for i in range(U_con_data.shape[1]):
        temp_U_con_data = deal_data(U_con_data,i,i)
        temp_con_divlist = div(temp_U_con_data)
        if con_entropy != (SCE_Entropy(temp_con_divlist, U_dec_divlist)):
            core_data = numpy.append(core_data, U_con_data[:, i,numpy.newaxis], axis=1)
            core_list.append(i)
    return core_list,core_data

def Red(core_data,red_list,U_dec_divlist,con_entropy):#约简
    B_data = core_data
    if SCE_Entropy(div(core_data),U_dec_divlist) == con_entropy:
        print("约简为",red_list)
        return core_data,red_list
    print(red_list)
    print(con_entropy,"条件属性的熵")
    attr_data, attr_list = del_dup(U_con_data, red_list)  # C-C0
    B_entropy =SCE_Entropy(div(B_data),U_dec_divlist)
    print(con_entropy, B_entropy, "f")
    dict = {}
    while con_entropy != B_entropy :

        dict.clear()
        con_key = -1  # 字典key
        con_value = -1  # 字典value
        for i in range(attr_data.shape[1]):
            temp_core_data = B_data
            temp_core_data = numpy.append(temp_core_data,attr_data[:,i,numpy.newaxis],axis=1)
            dict[i] = B_entropy - SCE_Entropy(div(temp_core_data),U_dec_divlist)
        # print(dict,attr_list)
        for key in dict:
            if dict[key] > con_value:
                con_value = dict[key]
                con_key = key
        B_data = numpy.append(B_data,attr_data[:,con_key,numpy.newaxis],axis=1)
        B_entropy =SCE_Entropy(div(B_data),U_dec_divlist)
        attr_data = deal_data(attr_data,con_key,con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
        print(B_entropy,"fffff")
    # print(attr_list)
    B_data,red_list = De_redundancy(B_data, red_list, U_dec_divlist, con_entropy)
    print(red_list,"red_list")
    return B_data,red_list

def De_redundancy(red_data,red_list,U_dec_divlist,con_entropy):# 去冗余
    i = 0
    while i < red_data.shape[1]:
        temp_Red_data = deal_data(red_data,i,i)
        red_entropy = SCE_Entropy(div(temp_Red_data),U_dec_divlist)
        if con_entropy == red_entropy:
            red_data = deal_data(red_data,i,i)
            del core_list[i]
            i = 0
            continue
        i += 1
    return red_data,red_list

if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile("../complete_dataSet_classication/lymph.txt")
    U_con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    U_dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    U_con_divlist = div(U_con_data)
    U_dec_divlist = div(U_dec_data)
    print(U_con_divlist,U_dec_divlist)
    con_entropy = SCE_Entropy(U_con_divlist,U_dec_divlist)
    # print(con_entropy,"con_entropy")
    core_list,core_data = core(U_con_data, U_dec_divlist,con_entropy)
    red_data,red_list = Red(core_data,core_list,U_dec_divlist,con_entropy)
    end = time.perf_counter()
    print(end - start)