'''
基于正域 正域加速
'''
import time
from itertools import chain

from part2.quote_file import div,deal_data,getCore_data,del_dup,data_add

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(' ')
        list_data.append(list_line)
    print(list_data)
    return list_data

def div_dec(my_data): #
    div_list =[]#返回的划分集合
    list1 = []
    for i in range(len(my_data)):  #
        list1.clear()
        if list(chain.from_iterable(div_list)).__contains__(i):  # 展开
            continue
        list1.append(i)
        for j in range(i + 1, len(my_data)):
            if ((my_data[i] == my_data[j])):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

def get_matrix(my_data): #多个对象的相容类等于单个对象的交集
    Sp_matrix = [[] for i in range(len(my_data))]
    for i in range(len(my_data)):
        for j in range(len(my_data[0])):
            sp_set = set()
            for k in range(len(my_data)):
                if len(eval(my_data[i][j]) & eval(my_data[k][j])) != 0:
                    sp_set.add(k)
            Sp_matrix[i].append(sp_set.copy())
    return Sp_matrix

def div_base_matric(Sp_matrix):  #相容类下用交集求划分
    sp_list = []
    for j in range(len(Sp_matrix)):
        sp = set(k for k in range(len(Sp_matrix)))
        for i in range(len(Sp_matrix[0])):
            sp = sp & Sp_matrix[j][i]
        sp_list.append(list(sp.copy()))
    return sp_list

def pos(dec_divlist,con_divlist):  #子集  正域集合   会快一点
    pos_list=[]
    temp_con_divlist = [con_divlist[i][:] for i in range(len(con_divlist))]
    for j in range(len(temp_con_divlist)-1,-1,-1):
        for i in dec_divlist:
            if set(temp_con_divlist[j]).issubset(i):
                pos_list += [j]
                del temp_con_divlist[j]
                break
    return  pos_list

def dependency(pos_list,my_data):#依赖度
     dep_num =  (len(pos_list) / len(my_data))
     # print("依赖度:",dep_num)
     return dep_num

def Red(con_data,dec_data):
    core_list = []
    red_data = getCore_data(core_list, con_data)  # core_data
    red_list = core_list.copy()
    temp_red_data = [red_data[i][:] for i in range(len(red_data))]
    temp_con_data = [con_data[i][:] for i in range(len(con_data))]
    temp_dec_data = [dec_data[i][:] for i in range(len(dec_data))]
    dict ={}
    attr_data,attr_list = del_dup(con_data,core_list)
    while dependency(pos(div(temp_dec_data),div(temp_red_data)),temp_con_data) != dependency(pos(div(temp_dec_data), div(temp_con_data)), temp_con_data):
        dict.clear()
        con_key = -1  # 字典key
        con_value = -10000  # 字典value
        pos_list = pos(div(dec_data),div(red_data))
        m = len(con_data) - 1
        temp_red_data = [red_data[i][:] for i in range(len(red_data))]
        temp_con_data = [con_data[i][:] for i in range(len(con_data))]
        temp_attr_data = [attr_data[i][:] for i in range(len(attr_data))]
        temp_dec_data = [dec_data[i][:] for i in range(len(dec_data))]
        while m >= 0:
            if set(pos_list).__contains__(m):  # 删除对象
                del temp_con_data[m]
                del temp_red_data[m]
                del temp_attr_data[m]
                del temp_dec_data[m]
            m -= 1
        for n in range(len(attr_data[0])):
            dict[n] = dependency(pos(div(temp_dec_data), div(data_add(temp_attr_data,temp_red_data,n))), temp_con_data)
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        temp_red_data = data_add(temp_attr_data,temp_red_data,con_key)
        red_data = data_add(attr_data,red_data,con_key)
        attr_data = deal_data(attr_data,con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
    print(red_list)
    return red_data,red_list

# def De_redundancy(Red_data,dec_divlist,dep_num,red_list):# 去冗余
#     i = 0
#     while i < len(Red_data[0]):
#         temp_Red_data = deal_data(Red_data,i)
#         dep = dependency(pos(dec_divlist, div(temp_Red_data)), Red_data)
#         if dep_num == dep:
#             Red_data = deal_data(Red_data,i)
#             del red_list[i]
#             i = 0
#             continue
#         i += 1
#     print(red_list,"去冗余red_list")



if __name__ == "__main__":
    start = time.perf_counter()
    list_data = readfileBylist("set_value.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    con_divlist = div_base_matric(get_matrix(con_data))
    dec_divlist = div_dec(dec_data)
    print("con_divlist", con_divlist)
    print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    print("pos_list",pos_list)
    dep_num = dependency(pos_list,list_data)
    print("dep_num",dep_num)
    red_data,red_list =Red(con_data,dec_data)
    # # De_redundancy(red_data,dec_divlist,dep_num,red_list)
    # end = time.perf_counter()
    # print(end - start)