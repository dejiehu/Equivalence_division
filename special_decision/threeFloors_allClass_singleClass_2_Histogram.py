import time
from itertools import product

import numpy
from sklearn.cluster import KMeans

'''
正域保持约简
'''
from part2.quote_file import div
from draw .drawing import draw,draw_Compare,draw_three,Histogram

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s=[]
        for j in range(len(list_line) ):
            s.append(int(list_line[j]))
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

def pos_specialDec(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for j in range(len(con_divlist)):
        # print(con_divlist[j],dec_divlist)
        if set(con_divlist[j]).issubset(dec_divlist):
            pos_list += con_divlist[j]    ############修改过
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
            if  not(({i}.issubset(set(pos_list)) or {j}.issubset(set(pos_list))) and dec_data[i] != dec_data[j]):
                continue
            if len(core) != 0 and is_existence(i, j, core):
                continue
            else:
                for k in range(len(con_data[0])):
                    if (con_data[i][k] != con_data[j][k]):
                        s.add(k)
                if len(s) == 1:
                    core += s
            if len(s)!=0:
                DM[i][j] = s.copy()
    # for i in DM:
    #     print(i)
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
    for j in fix:
        if j.issubset(dis):
            result_list.append(j)
            continue
        for i in dis:
            temp_j=j.copy()
            temp_j.add(i)
            result_list.append(temp_j)
    return result_list

def Red(DM):#逻辑运算d
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    difference_term = len(DM_list)
    # DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）

    # print(DM_list,len(DM_list),"多余集合被吸收")
    # loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    # for i in DM_list:
    #     loop_val.append(i)
    # DM_list = []
    # if len(loop_val) > 1: ###############################      修改过
    #     for i in loop_val[0]:
    #         DM_list.append({i})
    #     for i in range(1,len(loop_val)):
    #         DM_list = product1(DM_list,loop_val[i])
    #         DM_list = logic_operation(DM_list)
    # elif len(loop_val) == 0:
    #     DM_list = loop_val.copy()
    # elif len(loop_val[0]) == 1:
    #     DM_list = loop_val.copy()
    # elif len(loop_val[0]) > 1:
    #     for i in loop_val[0]:
    #         DM_list.append({i})
    return difference_term

def red_avgLength(red):
    print("约简的集合为：", len(red))
    num = 0
    if len(red) != 0:
        for i in red:
            num += len(i)
        print(num/len(red),"平均长度")

if __name__ == '__main__':
    T1 = time.perf_counter()
    # start = time.perf_counter()
    # list_data = readfileBylist("../complete_dataSet_classication/german.txt")
    list_data = readfileBylist("multi_dataSet_Numerical/abalone.csv")   #  连续处理
    # list_data = readfileBylist("multi_dataSet_artificial/")    #离散处理
    print(len(list_data),"对象数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 3)], list_data))
    print(len(con_data[0]), "条件属性数")
    dec_data_1 = list(map(lambda x: x[(len(list_data[0]) - 3):(len(list_data[0]) - 2)], list_data))
    dec_data_2 = list(map(lambda x: x[(len(list_data[0]) - 2):(len(list_data[0]) -1)], list_data))
    dec_data_3 = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    dec_divlist_1 = div(dec_data_1)
    dec_divlist_2 = div(dec_data_2)
    dec_divlist_3 = div(dec_data_3)

    #####找最小
    class_len_3 = len(dec_divlist_3[0])
    class_num_3 = 0
    for i in range(len(dec_divlist_3)):
        if class_len_3 > len(dec_divlist_3[i]):
            class_len_3 = len(dec_divlist_3[i])
            class_num_3 = i

    for i in range(len(dec_divlist_2)):
        if set(dec_divlist_3[class_num_3]).issubset(dec_divlist_2[i]):
            class_num_2 = i
            break

    for i in range(len(dec_divlist_1)):
        if set(dec_divlist_2[class_num_2]).issubset(dec_divlist_1[i]):
            class_num_1 = i
            break

    #####    全类
    time_list = []
    for i in range(10):
        # print(i)
        start = time.perf_counter()
        temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]
        con_divlist = div(temp_con_data)
        # pos_list = pos(dec_divlist_1,con_divlist)
        pos_list = pos(dec_divlist_1, con_divlist)
        DM = Matrix_construct(temp_con_data, pos_list, dec_data_1)
        difference_term = Red(DM)
        time_list.append(difference_term)
    # red_avgLength(reduct_list)
    # T2 = time.perf_counter()
    # print(T2-T1)
    # print("全类结果",reduct_list)

    print()
    ####    单类K=4
    time_list_1 = []
    x = []
    ############################
    # print("第一列选了：",(dec_divlist_1[class_num_1]))
    for i in range(10):
        x.append(i+1)
        start = time.perf_counter()
        temp_con_data = con_data[0:int(len(con_data)*(i+1)/10)]
        con_divlist = div(temp_con_data)
        pos_list = pos_specialDec(dec_divlist_1[class_num_1], con_divlist)
        DM = Matrix_construct(temp_con_data,pos_list,dec_data_1)
        difference_term = Red(DM)
        end = time.perf_counter()
        time_list_1.append(difference_term)
    # red_avgLength(reduct_list)
    # print("k=4", reduct_list)
    ######    单类K=8

    print()
    time_list_2 = []
    # print("第二列选了：",(dec_divlist_2[class_num_2]))
    for i in range(10):
        start = time.perf_counter()
        temp_con_data = con_data[0:int(len(con_data)*(i+1)/10)]
        con_divlist = div(temp_con_data)
        pos_list = pos_specialDec(dec_divlist_2[class_num_2], con_divlist)
        # print("pos_list",pos_list,len(pos_list))
        DM = Matrix_construct(temp_con_data,pos_list,dec_data_2)
        difference_term = Red(DM)
        end = time.perf_counter()
        time_list_2.append(difference_term)
    # red_avgLength(reduct_list)
    # print("k=8", reduct_list)
    print()
    ######    单类K=16
    # print("第三列选了：",(dec_divlist_3[class_num_3]))
    time_list_3 = []
    for i in range(10):
        start = time.perf_counter()
        temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]
        con_divlist = div(temp_con_data)
        pos_list = pos_specialDec(dec_divlist_3[class_num_3], con_divlist)
        # print("pos_list",pos_list,len(pos_list))
        DM = Matrix_construct(temp_con_data, pos_list, dec_data_3)
        difference_term = Red(DM)
        end = time.perf_counter()
        time_list_3.append(difference_term)
    # red_avgLength(reduct_list)
    # print("k=16", reduct_list)
    Histogram(x,time_list,time_list_1,time_list_2,time_list_3)

