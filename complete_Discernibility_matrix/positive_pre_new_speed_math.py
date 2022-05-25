import time
from itertools import product

import numpy
import sympy as sy
'''
正域保持约简
'''
from part2.quote_file import div

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data


def pos(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
                continue
    return pos_list

def is_existence(i,j,core): #判断其他对象在核属性上的属性值是否相等
    for c in core:
        if con_data[i][c] != con_data[j][c]:
            return True
    return False

def Matrix_construct(con_data,pos_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    core = []
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()

            if  not(({i}.issubset(set(pos_list)) or {j}.issubset(set(pos_list))) and dec_data[i][0] != dec_data[j][0]):
                continue
            if len(core) != 0 and is_existence(i,j,core):
                continue
            else:
                for k in range(len(con_data[0])):
                    if (con_data[i][k] != con_data[j][k]):
                        s.add(k)
                if len(s) == 1:
                    core += s
            if len(s) != 0:
                DM[i][j] = s.copy()
    print(core,"core")
    # for i in DM:
    #     print(i,"矩阵")
    return DM
'''
耗时间
'''
def logic_operation(diffItem_list):#析取，吸收
    DM_list = sorted(diffItem_list, key=lambda i: len(i), reverse=False)
    m = len(DM_list) - 1# 吸收多余的集合
    while m > 0: #m从后往前
        n = 0  #从前往后
        while n < m:
            if set(DM_list[n]).issubset(DM_list[m]):
                del DM_list[m]
                break
            n += 1
        m -= 1
    return DM_list

def product1(fix,dis):
    result_list =[]
    for i in dis:
        for j in fix:
            temp_j=j.copy()
            temp_j.add(i)
            result_list.append(temp_j)
    return result_list

def Red(DM):#逻辑运算d
    DM_list = []
    start0= time.perf_counter()
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,len(DM_list),"多余集合被吸收")
    letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']
    formula = ""

    for i in range(len(DM_list)):
        formula += ("(")
        for j in range(len(DM_list[i])):
            formula += (letter_list[list(DM_list[i])[j]])
            if j < len(DM_list[i]) - 1:
                formula += ("|")
            else:
                formula += (")")
        if i < len(DM_list) - 1:
            formula += ("&")
    print(time.perf_counter() - start0)
    disjunctive_normal = sy.to_dnf(formula, True,True)
    print(disjunctive_normal)
    disjunctive_normal = str(disjunctive_normal)
    disjunctive_normal = disjunctive_normal.replace('(', '')
    disjunctive_normal = disjunctive_normal.replace(')', '')
    disjunctive_normal = disjunctive_normal.replace('&', '')
    disjunctive_normal = disjunctive_normal.replace(' ', '')
    DM_list = []
    red = []
    for i in disjunctive_normal:
        if i == '|':
            DM_list.append(red)
            red = []
            continue
        red.append(letter_list.index(i))
    DM_list.append(red)






    print("约简的集合为：",len(DM_list), DM_list,"约简个数")
    num = 0
    for i in DM_list:
        num += len(i)
    print(num/len(DM_list),"平均长度")

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("../complete_dataSet_classication/zoo.txt")
    # list_data = readfileBylist("例子.txt")
    print(len(list_data),"对象数")
    print(len(list_data[0])-1,"条件属性数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    num_list = []
    for i in dec_data:
        if num_list.__contains__(i[0]):
            continue
        num_list.append(i[0])
    print(num_list,len(num_list),"决策数")
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)

    # print("con_divlist", con_divlist)
    # print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    print(pos_list.__len__())
    DM = Matrix_construct(con_data,pos_list,dec_data)
    Red(DM)

    end = time.perf_counter()
    print(end - start, "time")
