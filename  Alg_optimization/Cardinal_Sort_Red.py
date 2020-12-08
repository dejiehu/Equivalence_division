import os
import sys
import time
from itertools import chain
import numpy
# o_path = os.getcwd() # 返回当前工作目录
# sys.path.append(o_path) # 添加自己指定的搜索路径
# from part2 import
def readfile():     #读文件
    my_data = numpy.loadtxt('../cardinal.txt')
    my_data = my_data.astype(int)
    print(my_data)
    return my_data

def del_data(my_data,U_list,classTable_list):  #删除行元素
    temp_Table_list = classTable_list.copy()
    for i in range(my_data.shape[0]-1,-1,-1):
        if not(U_list.__contains__(i)):
            my_data = numpy.delete(my_data,i,axis = 0)
            del temp_Table_list[i]
    return my_data,temp_Table_list

def del_data_dec(my_data,U_list,classTable_list,dec_data):  #删除行元素
    temp_Table_list = classTable_list.copy()
    # print(U_list)
    for i in range(my_data.shape[0]-1,-1,-1):
        if not(U_list.__contains__(i)):
            my_data = numpy.delete(my_data, i, axis = 0)
            dec_data = numpy.delete(dec_data, i, axis=0)
            del temp_Table_list[i]
    return my_data,temp_Table_list,dec_data

def deal_data(my_data, m, n):  # 处理数据表  找出条件属性和决策属性用
    if n + 1 > m:
        for d in range(n, m - 1, -1):
            my_data = numpy.delete(my_data, d, 1)  # d为下标
    return my_data

def Max_min(con_data):  #找出属性最大最小值
    Mm_list = []
    for i in range(con_data.shape[1]):
        Mm_list.append([numpy.max(con_data[:, i]),numpy.min(con_data[:, i])])
    return Mm_list

def div(my_data,Mm_list):    #等价类的划分
    U_linkList = [i for i in range(len(my_data))]
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

def U_pos_nes(con_list,dec_data):    #求简化表
    Upos_list = []
    Uneg_list = []
    for i in con_list:
        for j in range(len(i)):
            if(dec_data[i[j]] != dec_data[i[0]]):
                Uneg_list.append(i[0])
                break
            if j == len(i)-1:
                Upos_list.append(i[0])
    return Upos_list,Uneg_list

def is_belongTo(con_list,Upos_list,lable_list):  #判断是否属于
    for i in con_list:
        if not Upos_list.__contains__(lable_list[i]):
            return False
    return True

def is_card_yes(con_list,dec_data):   # 判断基数是否为1
    for i in con_list:
        if dec_data[i] !=dec_data[0]:
            return False
    return True

def cal_Up(P_data,classTable_list,Upos_list,Uneg_list,dec_data):   #计算Up′
    X = div(P_data,Max_min(P_data))
    print(X)
    Up = []
    for i in X:
        # print(i)
        if is_belongTo(i,Upos_list,classTable_list):
            # print("is_belongTo")
            if is_card_yes(i,dec_data):
                Up = Up + i
        elif is_belongTo(i,Uneg_list,classTable_list):
            Up = Up + i
    return Up

def calculate(U_list,P_data,attr_data,Upos_list,Uneg_list,classTable_list,dec_data):
    if len(P_data) == 0:
        X_list = [U_list]
    else:
        # print(P_data)
        Up_list = cal_Up(P_data, classTable_list, Upos_list, Uneg_list, dec_data)
        print(classTable_list,"classTable_list")
        # print(Up_list,"Up_list")
        X_list = list(set(U_list).difference(set(Up_list)))     #U′ - Up′
        # print(X_list)
        X_data,P_Table_list = del_data(P_data, X_list, classTable_list)  #找出属性P的集合
        # print(X_data)
        X_list = div(X_data,Max_min(X_data))    # 对P进行划分(U′ - Up′)/P
    # print("P_Table_list",P_Table_list)
    print("X_list",X_list)
    sig_list = []
    Bp_list = []
    NBp_list = []
    for i_list in X_list:
        print(i_list,"i_list",classTable_list)
        # print(attr_data)
        temp_attr_data,temp_Table_list,temp_dec_data = del_data_dec(attr_data, i_list, classTable_list,dec_data)
        # print(temp_Table_list)
        Mm_list = [numpy.max(temp_attr_data[:, 0]),numpy.min(temp_attr_data[:, 0])]  #统计最大值最小值
        # print(Mm_list)
        bucket_list = [[]] * (Mm_list[0] - Mm_list[1] + 1)
        for i in i_list:              #将xi放入桶
            # print(i)
            bucket_list[temp_attr_data[i][0] - Mm_list[1]] = bucket_list[temp_attr_data[i][0] - Mm_list[1]] + [i]
            # print(bucket_list, "print(bucket_list)")
        # print(bucket_list)
        bucket_num = 0
        for j in bucket_list:
            # print(j)
            if len(j)!=0:
                # print(j,temp_Table_list)
                # print(is_belongTo(j,Upos_list,temp_Table_list) , is_card_yes(j,temp_dec_data))
                if is_belongTo(j,Upos_list,temp_Table_list) & is_card_yes(j,temp_dec_data):
                    Bp_list = Bp_list + j
                    # print("Upos")
                if is_belongTo(j,Uneg_list,temp_Table_list):
                    # print("Uneg")
                    NBp_list = NBp_list + j
    sig_list = Bp_list + NBp_list
    print("temp_Table_list",temp_Table_list)
    print("Bp_list,NBp_list",Bp_list,NBp_list)





if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile()
    classTable_list = [i for i in range(len(my_data))]  #对象标签
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    con_list = div(con_data, Max_min(con_data))
    Upos_list,Uneg_list = U_pos_nes(con_list, dec_data)   #
    my_data,classTable_list = del_data(my_data, Upos_list + Uneg_list,classTable_list)   #     简化的表+简化的标签对象
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)  #     简化的条件属性
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)  #     简化的决策属性

    # attr_data= deal_data(con_data,3,con_data.shape[1] - 1)
    attr_data = deal_data(con_data, 0, 2)
    # print(attr_data)

    # P_data= deal_data(con_data,1,con_data.shape[1] - 1)
    # P_data = deal_data(P_data, 0, 0)
    P_data =[]
    U_list = [i for i in range(len(con_data))]  # U′
    #
    calculate(U_list,P_data,attr_data,Upos_list,Uneg_list,classTable_list,dec_data)
    #
    #
    # end = time.perf_counter()
    # print(end - start)