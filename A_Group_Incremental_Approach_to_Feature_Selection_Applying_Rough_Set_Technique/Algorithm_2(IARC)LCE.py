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

def LCE_Entropy(con_divlist,dec_divlist):  #梁的熵
    U_list = list(chain.from_iterable(con_divlist))
    U_len = len(U_list)
    l_entropy = 0
    for i in con_divlist:
        for j in dec_divlist:
            i_c = (set(U_list).difference(set(i)))   #补集
            j_c = (set(U_list).difference(set(j)))   #补集
            if (len((set(i) & set(j))) != 0) & (len(j_c - i_c) != 0):
                l_entropy += (((len((set(i) & set(j)))/U_len) * (len(i_c & j_c))/U_len))
    # print(l_entropy,"l_entropy")
    return l_entropy

def U_Ux_LCE_Entropy(U_con_data,U_dec_data,Ux_con_data,Ux_dec_data):#梁的熵
    U_con_divlist = div(U_con_data)
    U_dec_divlist = div(U_dec_data)
    Ux_con_divlist = div(Ux_con_data)
    Ux_dec_divlist = div(Ux_dec_data)
    print(U_con_divlist,U_dec_divlist,"U_con_divlist,U_dec_divlist")
    U_len = U_con_data.shape[0]
    Ux_con_divlist = Add_Ux_dataShape(U_len, Ux_con_divlist)
    Ux_dec_divlist = Add_Ux_dataShape(U_len, Ux_dec_divlist)
    diff_len = merge_divlist(U_con_data,Ux_con_data,U_dec_data,Ux_dec_data,U_con_divlist,U_dec_divlist,Ux_con_divlist,Ux_dec_divlist)
    return (math.pow(U_len,2) * LCE_Entropy(U_con_divlist,U_dec_divlist) + 2 * diff_len)/math.pow(U_len + 1,2)

def merge_divlist(U_con_data,Ux_con_data,U_dec_data,Ux_dec_data,U_con_divlist,U_dec_divlist,Ux_con_divlist,Ux_dec_divlist):#      U/C + Ux/C
    U_Ux_con_divlist = []
    U_Ux_dec_divlist = []
    for i in range(len(Ux_con_divlist)-1,-1,-1):  #逆序循环
        for j in range(len(U_con_divlist)-1,-1,-1):
            if (U_con_data[U_con_divlist[j][0]] == Ux_con_data[(Ux_con_divlist[i][0]) - U_data.shape[0]]).all():
                U_Ux_con_divlist += (U_con_divlist[j] + Ux_con_divlist[i])
                break
    if len(U_Ux_con_divlist) == 0:
        U_Ux_con_divlist += Ux_con_divlist[0]
    for i in range(len(Ux_dec_divlist)-1,-1,-1):  #逆序循环
        for j in range(len(U_dec_divlist)-1,-1,-1):
            if (U_dec_data[U_dec_divlist[j][0]] == Ux_dec_data[(Ux_dec_divlist[i][0]) - U_data.shape[0]]).all():
                U_Ux_dec_divlist += (U_dec_divlist[j] + Ux_dec_divlist[i])
                break
    if len(U_Ux_dec_divlist) == 0:
        U_Ux_dec_divlist += Ux_dec_divlist[0]
    print(len(set(U_Ux_con_divlist) - set(U_Ux_dec_divlist)),U_Ux_con_divlist,U_Ux_dec_divlist,"len(set(U_Ux_con_divlist) - set(U_Ux_dec_divlist))")
    return len(set(U_Ux_con_divlist) - set(U_Ux_dec_divlist))

def pairs_of_object(x):  #类对的个数
    return x*(x-1)/2

def Add_Ux_dataShape(U_len,Ux_divlist):   #  调整增加的属性的对象序号
    for i in range(len(Ux_divlist)):
        for j in range(len(Ux_divlist[i])):
            Ux_divlist[i][j] += U_len
    return Ux_divlist



def Red(red_list,U_dec_divlist,con_entropy):#约简
    # if LCE_Entropy(div(red_data),U_dec_divlist) == con_entropy:
    #     print("约简为",red_list)
    #     return red_list
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
            dict[i] = LCE_Entropy(div(temp_core_data),U_dec_divlist)
        print(dict)
        for key in dict:
            if dict[key] < con_value:
                con_value = dict[key]
                con_key = key
        B_data = numpy.append(B_data,attr_data[:,con_key,numpy.newaxis],axis=1)
        B_entropy =LCE_Entropy(div(B_data),U_dec_divlist)
        attr_data = deal_data(attr_data,con_key,con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
    print(attr_list)
    print(red_list,"core_list")
    return B_data,red_list

if __name__ == '__main__':
    start = time.perf_counter()
    U_data = readfile("table_1.txt")
    Ux_data = readfile("add_single.txt")
    Ux_data = Ux_data.reshape(1,5)
    red_list = [0,1,3]
    U_con_data = deal_data(U_data, U_data.shape[1] - 1, U_data.shape[1] - 1)
    U_dec_data = deal_data(U_data, 0, U_data.shape[1] - 2)
    Ux_con_data = deal_data(Ux_data, Ux_data.shape[1] - 1, Ux_data.shape[1] - 1)
    Ux_dec_data = deal_data(Ux_data, 0, Ux_data.shape[1] - 2)
    U_Ux_LCE_Entropy(U_con_data,U_dec_data,Ux_con_data,Ux_dec_data)
    # core_list,core_data = core(U_con_data, U_dec_divlist,con_entropy)

    # red_data,red_list = Red(red_list,U_dec_divlist,con_entropy)
    end = time.perf_counter()
    print(end - start)