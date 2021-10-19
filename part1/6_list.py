import math
import time
from itertools import chain
import numpy
from part2.quote_file import div,deal_data,getCore_data,del_dup,data_add

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(' ')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data

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
            insection = set(j) & set(k)
            if len(insection) != 0:
                s.append(list(insection))
        con_entropy += ((len(j)/U_num) * Entropy(s,j))
    return con_entropy

def core(con_data, dec_divlist,con_entropy):  #基于条件熵求核
    core_list = []
    for i in range(len(con_data[0]) - 1, -1, -1):
        temp_con_data = deal_data(con_data, i)
        temp_con_divlist = div(temp_con_data)
        if con_entropy != (con_Entropy(temp_con_divlist, dec_divlist)):
            print("核属性是第",i,"个")
            core_list.append(i)
    print(core_list,"核属性")
    return core_list

def Red(dec_divlist,con_entropy,con_data):#约简
    core_data = getCore_data(core_list,con_data)
    if len(core_list) == 0:
        print("无约简")
        return
    B = core_data
    if con_Entropy(div(core_data),dec_divlist) == con_entropy:
        print("约简为",core_list)
        return
    red_entropy = -1
    dict = {}
    Red_data = [core_data[i][:] for i in range(len(core_data))]
    attr_data, attr_list = del_dup(con_data, core_list)
    red_list = core_list.copy()
    while con_entropy != red_entropy:
        dict.clear()
        con_key = -1  # 字典key
        con_value = 10000000  # 字典value
        for k in range(len(attr_data[0])):
            temp_Red_data = data_add(attr_data,Red_data,k)
            print(temp_Red_data)
            dict[k] = con_Entropy(div(temp_Red_data),dec_divlist)
        for key in dict:
            if con_value > dict[key]:
                con_value = dict[key]
                con_key = key
        Red_data = data_add(attr_data, Red_data, con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
        attr_data = deal_data(attr_data, con_key)
        red_entropy =con_Entropy(div(Red_data),dec_divlist)
    print(red_list, "red_list")


if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("..\data.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist",con_divlist)
    print("dec_divlist", dec_divlist)
    con_entropy = con_Entropy(con_divlist,dec_divlist)
    print("条件熵：",con_entropy)
    core_list = core(con_data, dec_divlist,con_entropy)
    Red(dec_divlist,con_entropy,con_data)
    end = time.perf_counter()
    print(end - start)