import time
from itertools import product

import numpy
'''
正域保持约简
'''
from part2.quote_file import div

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(',')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data

def generalized_decision(con_divlist,dec_data):
    gd_list=[]
    div_dec = []
    for i in con_divlist:
        gd_set = set()
        for j in i:
            gd_set.add(dec_data[j][0])
        div_dec.append(list(gd_set))
    for i in range(len(dec_data)):
        for j in range(len(con_divlist)):
            if con_divlist[j].__contains__(i):
                gd_list.append(div_dec[j])
    print(gd_list)
    return gd_list

def Matrix_construct(con_data,gd_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(len(con_data)):
            s.clear()
            #全决策1
            if  gd_list[i].__contains__(dec_data[j][0]):
                continue
            for k in range(len(con_data[0])):
                if (con_data[i][k] != con_data[j][k]):
                    s.add(k)
            if len(s)!=0:
                DM[i][j] = s.copy()
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

def Red(DM):#逻辑运算d
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(len(DM)):
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
    print("约简的集合为：",len(DM_list), DM_list,"约简个数")
    num = 0
    for i in DM_list:
        num += len(i)
    print(num/len(DM_list),"平均长度")

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("../Qualitative_Bankruptcy.txt")
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
    gd_list = generalized_decision(con_divlist, dec_data)
    # print("con_divlist", con_divlist)
    # print("dec_divlist", dec_divlist)

    DM = Matrix_construct(con_data,gd_list,dec_data)
    Red(DM)

    end = time.perf_counter()
    print(end - start, "time")
