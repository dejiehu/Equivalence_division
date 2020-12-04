import time
from itertools import chain
import numpy

def readfile():     #读文件
    my_data = numpy.loadtxt('../cardinal.txt')
    my_data = my_data.astype(int)
    print(my_data)
    return my_data

def del_data(my_data,U_list,classTable_list):  #删除行元素
    for i in range(my_data.shape[0]-1,-1,-1):
        if not(U_list.__contains__(i)):
            my_data = numpy.delete(my_data,i,axis = 0)
            del classTable_list[i]
    print(my_data, "\n", classTable_list)
    return my_data,classTable_list

def deal_data(my_data, m, n):  # 处理数据表  找出条件属性和决策属性用
    if n + 1 > m:
        for d in range(n, m - 1, -1):
            my_data = numpy.delete(my_data, d, 1)  # d为下标
    return my_data

def Max_min(con_data):  #找出最大最小值
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
        if not Upos_list.__contains__(lable_list[0]):
            return False
    return True

def is_card_yes(con_list,dev_data,lable_list):   # 判断基数是否为1
    for i in con_list:
        if dev_data[i] !=dec_data[0]:
            return False
    return True

def Up(P_data,classTable_list,Upos_list,Uneg_list,dev_data):   #计算Up′
    X = div(P_data,Max_min(P_data))
    print(X)
    Up = []
    for i in X:
        print(i)
        if is_belongTo(i,Upos_list,classTable_list):
            print("is_belongTo")
            if is_card_yes(i,dev_data,classTable_list):
                Up = Up + i
        elif is_belongTo(i,Uneg_list,classTable_list):
            Up = Up + i
    print(Up)

# def calculate():




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
    P_data = deal_data(con_data,1,con_data.shape[1] - 1)
    Up(P_data, classTable_list, Upos_list, Uneg_list,dec_data)



    end = time.perf_counter()
    print(end - start)