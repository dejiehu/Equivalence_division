import time
from itertools import product, chain
import operator
import numpy

from draw.drawing import draw_three_universe

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

def distribution(dec_divlist,con_divlist):  #
    distribution_list=[]
    for i in range(len(con_divlist)):
         S_tuple = ()
         for j in range(len(dec_divlist)):
             S_tuple = S_tuple + ((len(set(con_divlist[i]) & set(dec_divlist[j])))/len(con_divlist[i]),)
         distribution_list += [S_tuple]
    return distribution_list

def distribution_specialDec(dec_list,con_divlist):  #子集  正域
    distribution_list=[]
    for i in range(len(con_divlist)):
        S_tuple = ()
        S_tuple = S_tuple + ((len(set(con_divlist[i]) & set(dec_list))) / len(con_divlist[i]),)
        distribution_list += [S_tuple]
    return distribution_list

def Matrix_construct(con_data,distribution_list):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            if operator.eq(distribution_list[i],distribution_list[j]):
                continue
            for k in range(len(con_data[0])):
                if len(eval(con_data[i][k]) & eval(con_data[j][k])) == 0:
                    s.add(k)
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
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,len(DM_list),"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    DM_list = []
    if len(loop_val) > 1:  ###############################      修改过
        for i in loop_val[0]:
            DM_list.append({i})
        for i in range(1, len(loop_val)):
            DM_list = product1(DM_list, loop_val[i])
            DM_list = logic_operation(DM_list)
    elif len(loop_val) == 0:
        DM_list = loop_val.copy()
    elif len(loop_val[0]) == 1:
        DM_list = loop_val.copy()
    elif len(loop_val[0]) > 1:
        for i in loop_val[0]:
            DM_list.append({i})
    return DM_list

def red_avgLength(red):
    print("约简的集合为：",red)
    num = 0
    if len(red) != 0:
        for i in red:
            num += len(i)
        print(len(red),"   ",num/len(red),"平均长度")
    print()

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("set_value_datasets/5%/lymphography.csv")
    # list_data = readfileBylist("Parameters comparison/10%/Real estate valuation.csv")
    print(len(list_data), "对象数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    print(len(con_data[0]), "条件属性数")

    con_divlist = div_byCompare(con_data)
    dec_divlist = div_dec(dec_data)
    # print(con_divlist)
    # print(dec_divlist)
    # distribution_list = distribution(dec_divlist,con_divlist)
    distribution_list = distribution_specialDec(dec_divlist[0], con_divlist)
    # print(distribution_list)

    red = Red(Matrix_construct(con_data, distribution_list))
    print("全类：",len(dec_divlist))
    print("单特定类：",len(dec_divlist[0]),len(dec_divlist[1]))
    print("多特定类：")

    x = []
    time_list = []
    time_list_1 = []
    time_list_2 = []
    for i in range(10):
        x.append(i + 1)
        temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]
        con_divlist = div_byCompare(temp_con_data)
        start = time.perf_counter()
        #全类
        distribution_list = distribution(dec_divlist, con_divlist)
        print(distribution_list)
        DM = Matrix_construct(temp_con_data,distribution_list)
        reduct_list = Red(DM)
        time_list.append(time.perf_counter() - start)
        #单特定类
        start_1 = time.perf_counter()
        distribution_list_1 = distribution_specialDec(dec_divlist[2], con_divlist)
        print(distribution_list_1)
        DM_1 = Matrix_construct(temp_con_data, distribution_list_1)
        reduct_list_1 = Red(DM_1)
        time_list_1.append(time.perf_counter() - start_1)
        #多特定类
        start_2 = time.perf_counter()
        distribution_list_2 = distribution([dec_divlist[2]] + [dec_divlist[0]], con_divlist)
        DM_2 = Matrix_construct(temp_con_data, distribution_list_2)
        reduct_list_2 = Red(DM_2)
        time_list_2.append(time.perf_counter() - start_2)
        print("----",(i+1)*10,"%----")
    print("全类：")
    red_avgLength(reduct_list)
    print("单特定类:")
    red_avgLength(reduct_list_1)
    print("多特定类:")
    red_avgLength(reduct_list_2)
    draw_three_universe(x,time_list,time_list_1,time_list_2)