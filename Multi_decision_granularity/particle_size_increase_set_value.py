import time
from itertools import product, chain

import numpy
'''
正域保持约简
'''

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

def pos_specialDec(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for j in range(len(con_divlist)):
        if set(con_divlist[j]).issubset(dec_divlist):
            pos_list += con_divlist[j]
            continue
    # print(pos_list,"pos_list")
    return pos_list

def Matrix_construct(con_data,pos_list):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            if {i}.issubset(set(pos_list)) and {j}.issubset(set(pos_list)):
                continue
            if not({i}.issubset(set(pos_list))) and not({j}.issubset(set(pos_list))):
                continue
            for k in range(len(con_data[0])):
                if len(eval(con_data[i][k]) & eval(con_data[j][k])) == 0:
                    s.add(k)
            DM[i][j] = s.copy()
    print(DM)
    return DM
'''
耗时间
'''
def logic_operation(diffItem_list):#析取，吸收
    DM_list = []
    for i in diffItem_list:  #排序
        if len(DM_list) != 0:  # 列表不等0要找位置插入
            k = 0
            while k < len(DM_list):
                if len(set(i)) <= len(set(DM_list[k])):
                    DM_list.insert(k, i)
                    break
                k += 1
            if k == len(DM_list):
                DM_list.append(i)
        else:  # 列表为空直接加入
            DM_list.append(i)
    m = len(DM_list) - 1# 吸收多余的集合
    while m > 0: #m从后往前
        n = 0  #从前往后
        while n < m:
            # print(DM_list[n],DM_list[m],DM_list[n].issubset(DM_list[m]))
            if set(DM_list[n]).issubset(DM_list[m]):
                del DM_list[m]
                m = len(DM_list)
                break
            n += 1
        m -= 1
    return DM_list

def Red(DM):#逻辑运算
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,len(DM_list),"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    DM_list = []
    for i in product(*loop_val):
        DM_list.append(set(i))
    DM_list = logic_operation(DM_list)
    print("约简的集合为：",len(DM_list), DM_list)

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("set_value.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    con_divlist = div_base_matric(get_matrix(con_data))
    dec_divlist = div_dec(dec_data)
    print("con_divlist", con_divlist)
    print("dec_divlist", dec_divlist)
    pos_list = pos_specialDec(dec_divlist[0] + dec_divlist[1],con_divlist)
    print(pos_list)
    DM = Matrix_construct(con_data,pos_list)
    Red(DM)
    end = time.perf_counter()
    print(end - start, "time")
