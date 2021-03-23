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

def Entropy(attr_divlist,j):#信息熵
    entropy = 0
    for i in attr_divlist:
        p = len(i)/len(j)
        entropy -= p*math.log10(p)
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

def U_Ux_SCE_Entropy(U_con_data,U_dec_data,Ux_con_data,Ux_dec_data):
    U_con_divlist = div(U_con_data)
    U_dec_divlist = div(U_dec_data)
    Ux_con_divlist = div(Ux_con_data)
    Ux_dec_divlist = div(Ux_dec_data)
    U_len = U_con_data.shape[0]
    Ux_len = Ux_con_data.shape[0]
    Ux_con_divlist = Add_Ux_dataShape(U_len, Ux_con_divlist)
    Ux_dec_divlist = Add_Ux_dataShape(U_len, Ux_dec_divlist)
    U_Ux_con_divlist,U_comb_con_divlist,Ux_comb_con_divlist,U_Ux_U_con_divlist,U_Ux_Ux_con_divlist = merge_divlist(
        U_con_data,Ux_con_data,copy.deepcopy(U_con_divlist),copy.deepcopy(Ux_con_divlist))
    U_Ux_dec_divlist, U_comb_dec_divlist, Ux_comb_dec_divlist, U_Ux_U_dec_divlist, U_Ux_Ux_dec_divlist = merge_divlist(
        U_dec_data, Ux_dec_data, copy.deepcopy(U_dec_divlist) , copy.deepcopy(Ux_dec_divlist))
    latter = 0
    for i in range(len(U_Ux_con_divlist)):
        for j in range(len(U_Ux_dec_divlist)):
            print(U_Ux_dec_divlist,j)
            if len(U_comb_con_divlist[i]) * len(set(U_Ux_con_divlist[i]) & set(U_Ux_dec_divlist[j])) / len(U_Ux_con_divlist[i]) * len(set(U_comb_con_divlist[i]) & set(U_comb_dec_divlist[j])) == 0:
                continue
            if len(Ux_comb_con_divlist[i]) * len(set(U_Ux_con_divlist[i]) & set(U_Ux_dec_divlist[j])) / len(U_Ux_con_divlist[i]) * len(set(Ux_comb_con_divlist[i]) & set(Ux_comb_dec_divlist[j])) == 0:
                continue
            print("进")
            latter += (len(set(U_comb_con_divlist[i])&set(U_comb_dec_divlist[j])) / (U_len + Ux_len)) * \
                      math.log10(len(U_comb_con_divlist[i]) * len(set(U_Ux_con_divlist[i]) & set(U_Ux_dec_divlist[j])) /
                                 len(U_Ux_con_divlist[i]) * len(set(U_comb_con_divlist[i]) & set(U_comb_dec_divlist[j]))) + \
                      (len(set(Ux_comb_con_divlist[i])&set(Ux_comb_dec_divlist[j])) / (U_len + Ux_len)) * \
                      math.log10(len(Ux_comb_con_divlist[i]) * len(set(U_Ux_con_divlist[i]) & set(U_Ux_dec_divlist[j])) /
                                 len(U_Ux_con_divlist[i]) * len(set(Ux_comb_con_divlist[i]) & set(Ux_comb_dec_divlist[j])))
        print(latter,"latter")
        for k in range(len(U_Ux_U_dec_divlist)):
            latter += (len(set(U_comb_con_divlist[i])&set(U_Ux_U_dec_divlist[k])) / (U_len + Ux_len)) * \
                      math.log10(len(U_comb_con_divlist[i]) / len(U_Ux_con_divlist[i]))
        print(latter, "latter")
        for l in range(len(U_Ux_Ux_dec_divlist)):
            latter += (len(set(Ux_comb_con_divlist[i])&set(U_Ux_Ux_dec_divlist[l])) / (U_len + Ux_len)) * \
                      math.log10(len(Ux_comb_con_divlist[i]) / len(U_Ux_con_divlist[i]))
        print(latter, "latter")
    print((U_len , SCE_Entropy(U_con_divlist,U_dec_divlist) , Ux_len , SCE_Entropy(Ux_con_divlist,Ux_dec_divlist)),(U_len + Ux_len) , latter,"last")
    return (U_len * SCE_Entropy(U_con_divlist,U_dec_divlist) + Ux_len * SCE_Entropy(Ux_con_divlist,Ux_dec_divlist))/(U_len + Ux_len) - latter

def merge_divlist(U_data,Ux_data,U_divlist,Ux_divlist):#      U/C + Ux/C
    U_comb_divlist = []
    Ux_comb_divlist = []
    U_Ux_divlist = []
    for i in range(len(Ux_divlist)-1,-1,-1):  #逆序循环
        for j in range(len(U_divlist)-1,-1,-1):
            if (U_data[U_divlist[j][0]] == Ux_data[(Ux_divlist[i][0]) - U_data.shape[0]]).all():
                U_comb_divlist.append(U_divlist[j])
                Ux_comb_divlist.append(Ux_divlist[i])
                U_Ux_divlist.append(U_divlist[j] + Ux_divlist[i])
                del U_divlist[j]
                del Ux_divlist[i]
                break
    return U_Ux_divlist,U_comb_divlist,Ux_comb_divlist,U_divlist,Ux_divlist #组合的列表

def Add_Ux_dataShape(U_len,Ux_divlist):   #  调整增加的属性的对象序号
    for i in range(len(Ux_divlist)):
        for j in range(len(Ux_divlist[i])):
            Ux_divlist[i][j] += U_len
    return Ux_divlist

def Red(red_list,U_dec_divlist,con_entropy):#约简
    print(con_entropy,"条件属性的熵")
    attr_data, attr_list = del_dup(U_con_data, red_list)  # C-C0
    B_entropy = -1
    dict = {}
    while con_entropy - B_entropy > 0.000001:
        print(con_entropy-B_entropy,"fffff")
        dict.clear()
        con_key = -1  # 字典key
        con_value = 100000  # 字典value
        for i in range(attr_data.shape[1]):
            temp_core_data = B_data
            temp_core_data = numpy.append(temp_core_data,attr_data[:,i,numpy.newaxis],axis=1)
            dict[i] = U_Ux_SCE_Entropy(div(temp_core_data),U_dec_divlist)
        print(dict)
        for key in dict:
            if dict[key] < con_value:
                con_value = dict[key]
                con_key = key
        B_data = numpy.append(B_data,attr_data[:,con_key,numpy.newaxis],axis=1)
        B_entropy =U_Ux_SCE_Entropy(div(B_data),U_dec_divlist)
        attr_data = deal_data(attr_data,con_key,con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
    print(attr_list)
    print(red_list,"core_list")
    return B_data,red_list

if __name__ == '__main__':
    start = time.perf_counter()
    U_data = readfile("table_1.txt")
    Ux_data = readfile("add_multiple.txt")
    red_list = [0,1,3]
    U_con_data = deal_data(U_data, U_data.shape[1] - 1, U_data.shape[1] - 1)
    U_dec_data = deal_data(U_data, 0, U_data.shape[1] - 2)
    Ux_con_data = deal_data(Ux_data, Ux_data.shape[1] - 1, Ux_data.shape[1] - 1)
    Ux_dec_data = deal_data(Ux_data, 0, Ux_data.shape[1] - 2)
    U_Ux_SCE_Entropy(U_con_data,U_dec_data,Ux_con_data,Ux_dec_data)
    # core_list,core_data = core(U_con_data, U_dec_divlist,con_entropy)

    # red_data,red_list = Red(red_list,U_dec_divlist,con_entropy)
    end = time.perf_counter()
    print(end - start)