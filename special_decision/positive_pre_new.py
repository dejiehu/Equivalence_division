import time
from itertools import product

import numpy
from sklearn.cluster import KMeans

'''
正域保持约简
'''
from part2.quote_file import div
from draw .drawing import draw,draw_Compare

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s=[]
        for j in range(len(list_line) - 1):
            s.append(int(list_line[j]))
        s.append(float(list_line[len(list_line) - 1]))
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
        if set(con_divlist[j]).issubset(dec_divlist):
            pos_list += [j]
            continue
    return pos_list

def Matrix_construct(con_data,pos_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            if  not(({i}.issubset(set(pos_list)) or {j}.issubset(set(pos_list))) and dec_data[i] != dec_data[j]):
                continue
            for k in range(len(con_data[0])):
                if (con_data[i][k] != con_data[j][k]):
                    s.add(k)
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
    for i in dis:
        for j in fix:
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
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    # print(DM_list,len(DM_list),"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    DM_list = []
    if len(loop_val) > 1:
        DM_list += [loop_val[0]]
        for i in range(1,len(loop_val)):
            DM_list = product1(DM_list,loop_val[i])
            DM_list = logic_operation(DM_list)

    # print("约简的集合为：",len(DM_list), DM_list,"约简个数")
    # num = 0
    # for i in DM_list:
    #     num += len(i)
    # print(num/len(DM_list),"平均长度")

if __name__ == '__main__':
    # start = time.perf_counter()
    # list_data = readfileBylist("../complete_dataSet_classication/german.txt")
    list_data = readfileBylist("../Numerical_decision_dataSet/Combined Cycle Power Plant.csv")
    print(len(list_data),"对象数")
    print(len(list_data[0])-1,"条件属性数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    # print(dec_data)
    # print(con_data)
    K=3
    y_pred = KMeans(n_clusters=K, max_iter=600).fit_predict(dec_data)
    print(y_pred, "划分结果",len(y_pred),(type(y_pred)))
    dec_divlist = [[]] * K
    for i in range(len(y_pred)):
        dec_divlist[y_pred[i]] = dec_divlist[y_pred[i]] + [i]

    # print(dec_divlist)

    time_list = []
    x = []
    for i in range(10):
        x.append(i+1)
        start = time.perf_counter()
        temp_con_data = con_data[0:int(len(con_data)*(i+1)/10)]
        con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist,con_divlist)
        DM = Matrix_construct(temp_con_data,pos_list,y_pred)
        Red(DM)
        end = time.perf_counter()
        time_list.append(end - start)
        # print(end - start, "time")
    time_list1 = []
    class_len = len(dec_divlist[0])
    for i in range(len(dec_divlist)):
        if class_len >= len(dec_divlist[i]):
            small_len = i
    print(len(dec_divlist[small_len]),"最小的类")
    for i in range(10):
        start1 = time.perf_counter()
        temp_con_data = con_data[0:int(len(con_data)*(i+1)/10)]
        con_divlist =div(temp_con_data)
        pos_list = pos_specialDec(dec_divlist[small_len],con_divlist)
        # print(len(dec_divlist[0]))
        DM = Matrix_construct(temp_con_data,pos_list,y_pred)
        Red(DM)
        end1 = time.perf_counter()
        time_list1.append(end1 - start1)
        # print(end - start, "time")
print(time_list)
print(time_list1)
draw_Compare(x,time_list,time_list1)

