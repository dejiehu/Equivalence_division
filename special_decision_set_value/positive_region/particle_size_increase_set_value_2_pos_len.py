import time
from itertools import product, chain

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
        list_line = list_row[i].strip().split('\t')
        list_data.append(list_line)
    # print(list_data)
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

def div_byCompare(my_data):
    sp_list = []
    for i in range(len(my_data)):
        sp = []
        for j in range(len(my_data)):
            if insection_isEmpty(i,j,my_data):
                sp.append(j)
        sp_list.append(sp)

    return sp_list

def insection_isEmpty(i,j,my_data):
    if i == j :
        return True
    for k in range(len(my_data[0])):
        if len(eval(my_data[i][k]) & eval(my_data[j][k])) == 0:
            return None
    return True

def pos(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for i in range(len(dec_divlist)):
         for j in range(len(con_divlist)):
            if set(con_divlist[j]).issubset(dec_divlist[i]):
                pos_list += [j]
                continue
    return pos_list

def pos_specialDec(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for j in range(len(con_divlist)):
        if set(con_divlist[j]).issubset(dec_divlist):
            pos_list += [j]
            continue
    # print(pos_list,"pos_list")
    return pos_list

def Matrix_construct(con_data,pos_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            if not (({i}.issubset(set(pos_list)) or {j}.issubset(set(pos_list))) and dec_data[i] != dec_data[j]):
                continue
            for k in range(len(con_data[0])):
                if len(eval(con_data[i][k]) & eval(con_data[j][k])) == 0:
                    s.add(k)
            DM[i][j] = s.copy()
    # print(DM)
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

def Red(DM):#逻辑运算
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    print((len(DM_list)/(len(DM)**2)*200))
    return (len(DM_list)/(len(DM)**2)*200)
    # DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    # print(DM_list,len(DM_list),"多余集合被吸收")
    # return DM_list

def red_avgLength(red):
    print("约简的集合为：", len(red),red)
    num = 0
    if len(red) != 0:
        for i in red:
            num += len(i)
        print(num/len(red),"平均长度")
    print()


def print_pos(pos_list):
    print("正域：",pos_list)
    print("正域长度：",len(pos_list))



if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("../set_value_dataSet(5%)在修改/Image_Segmentation(2100).csv")
    print(len(list_data), "对象数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 3)], list_data))
    print(len(con_data[0]), "条件属性数")
    dec_data_1 = list(map(lambda x: x[(len(list_data[0]) - 3):(len(list_data[0]) - 2)], list_data))
    dec_data_2 = list(map(lambda x: x[(len(list_data[0]) - 2):(len(list_data[0]) - 1)], list_data))
    dec_data_3 = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    dec_divlist_1 = div_dec(dec_data_1)
    dec_divlist_2 = div_dec(dec_data_2)
    dec_divlist_3 = div_dec(dec_data_3)

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
    # print("第一，", len(dec_divlist_1[class_num_1]), dec_divlist_1[class_num_1])
    # print("第二，", len(dec_divlist_2[class_num_2]), dec_divlist_2[class_num_2])
    # print("第三，", len(dec_divlist_3[class_num_3]), dec_divlist_3[class_num_3])
    x = []
    for i in range(10):
        x.append(i + 1)
        temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]
    #
    ####    全类
    # print("全类，K=4：")
    con_divlist = div_byCompare(con_data)
    pos_list = pos(dec_divlist_1, con_divlist)
    print_pos(pos_list)

    ###    单类K=4
    # print("\n单类，K=4：")
    pos_list_1 = pos_specialDec(dec_divlist_1[class_num_1], con_divlist)
    print_pos(pos_list_1)
    ######    单类K=8
    # print("\n单类，K=8：")
    pos_list_2 = pos_specialDec(dec_divlist_2[class_num_2], con_divlist)
    # print("pos_list",pos_list,len(pos_list))
    print_pos(pos_list_2)
    ######    单类K=16
    # print("\n单类，K=16：")
    pos_list_3 = pos_specialDec(dec_divlist_3[class_num_3], con_divlist)
    print_pos(pos_list_3)
    # Histogram(reduct_list, reduct_list_1, reduct_list_2, reduct_list_3)

    # x = []
    # time_list = []
    # time_list_1 = []
    # time_list_2 = []
    # time_list_3 = []
    # for i in range(10):
    #     x.append(i + 1)
    #     temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]
    #     con_divlist = div_byCompare(temp_con_data)
    #     start = time.perf_counter()
    #     pos_list = pos(dec_divlist_1, con_divlist)
    #     DM = Matrix_construct(temp_con_data, pos_list, dec_data_1)
    #     reduct_list = Red(DM)
    #     time_list.append(reduct_list)
    #     ###    单类K=4
    #     start_1 = time.perf_counter()
    #     pos_list_1 = pos_specialDec(dec_divlist_1[class_num_1], con_divlist)
    #     DM_1 = Matrix_construct(temp_con_data, pos_list_1, dec_data_1)
    #     reduct_list_1 = Red(DM_1)
    #     time_list_1.append(reduct_list_1)
    #     ######    单类K=8
    #     start_2 = time.perf_counter()
    #     pos_list_2 = pos_specialDec(dec_divlist_2[class_num_2], con_divlist)
    #     # print("pos_list",pos_list,len(pos_list))
    #     DM_2 = Matrix_construct(temp_con_data, pos_list_2, dec_data_2)
    #     reduct_list_2 = Red(DM_2)
    #     time_list_2.append(reduct_list_2)
    #     ######    单类K=16
    #     start_3 = time.perf_counter()
    #     pos_list_3 = pos_specialDec(dec_divlist_3[class_num_3], con_divlist)
    #     DM_3 = Matrix_construct(temp_con_data, pos_list_3, dec_data_3)
    #     reduct_list_3 = Red(DM_3)
    #     time_list_3.append(reduct_list_3)
    # Histogram(x, time_list, time_list_1, time_list_2, time_list_3)