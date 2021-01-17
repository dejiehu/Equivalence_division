
import time
from itertools import chain
import numpy

from draw.drawing import draw


def readfile():     #读文件
    my_data = numpy.loadtxt('../german.txt')
    my_data = my_data.astype(int)
    print(my_data)
    print("*******************************************************************")
    return my_data

def deal_data(my_data, m, n):  # 处理数据表  找出条件属性和决策属性用
    if n + 1 > m:
        for d in range(n, m - 1, -1):
            my_data = numpy.delete(my_data, d, 1)  # d为下标
    return my_data

def Max_min(con_data,U_list):  #找出属性最大最小值
    Mm_list = []
    for i in range(con_data.shape[1]):
        min = 10000
        Max = 0
        for j in U_list:
            if con_data[j][i] > Max:
                Max = con_data[j][i]
            if con_data[j][i] < min:
                min = con_data[j][i]
        Mm_list.append([Max,min])
    return Mm_list

def div(my_data,U_list):    #等价类的划分
    U_linkList = U_list.copy()
    Mm_list = Max_min(my_data,U_linkList)
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

def is_belongTo(con_list,Upos_list):  #判断是否属于
    for i in con_list:
        if not Upos_list.__contains__(i):
            return False
    return True

def is_card_yes(con_list,dec_data):   # 判断基数是否为1
    for i in con_list:
        if not(dec_data[i] == dec_data[con_list[0]]).all():
            return False
    return True

def cal_Up(U_list,P_data,Upos_list,Uneg_list,dec_data):
    X = div(P_data,U_list)
    Up = []
    for i_list in X:
        if is_belongTo(i_list,Upos_list) & is_card_yes(i_list,dec_data):
            Up = Up + i_list
        elif is_belongTo(i_list,Uneg_list):
            Up = Up + i_list
    return Up

def calculate(U_list,P_data,attr_data,Upos_list,Uneg_list,dec_data):
    if P_data.shape[1] == 0:
        X_list = [U_list.copy()]
    else:
        Up_list = cal_Up(U_list,P_data,Upos_list,Uneg_list,dec_data)
        X_list = div(P_data,list(set(U_list).difference(set(Up_list))))    #(U′ - Up′)/a
    sig_list = []
    Bp_list = []
    NBp_list = []
    UPa_divlist = []
    for j_list in X_list:
        temp_UPa_divlist = div(attr_data,j_list)
        UPa_divlist = UPa_divlist + temp_UPa_divlist
    for i_list in UPa_divlist:
        if is_belongTo(i_list,Upos_list) & is_card_yes(i_list,dec_data):
            Bp_list = Bp_list + i_list
        if is_belongTo(i_list,Uneg_list):
            NBp_list = NBp_list + i_list
    sig_list = Bp_list + NBp_list
    return sig_list,Bp_list,NBp_list,UPa_divlist

def Reduce_basedSig(my_data):
    if len(my_data) == 0:
        print("无数据")
        return
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    U_list = [i for i in range(len(my_data))]
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    con_list = div(con_data,U_list)      #U/C
    print(len(con_list))
    Upos_list,Uneg_list = U_pos_nes(con_list, dec_data)   #   U'pos    U'neg
    U_list = Upos_list + Uneg_list    #  U'
    attr_data = con_data
    R_data = numpy.empty(shape=(my_data.shape[0],0))   #约简
    R_data = R_data.astype(int)
    num = 0
    while len(U_list) != 0:
        num += 1
        sig_num = 0
        sig_list = []
        Bp_list = []
        NBp_list = []
        UPa_divlist =[]
        n = -1
        i = 0
        while i < attr_data.shape[1]:
            temp_sig_list, temp_Bp_list, temp_NBp_list, temp_UPa_divlist = \
                calculate(U_list.copy(), R_data, attr_data[:,i,numpy.newaxis], Upos_list, Uneg_list, dec_data)
            if len(temp_sig_list) > sig_num:
                n = i
                sig_num = len(temp_sig_list)
                sig_list = temp_sig_list
                Bp_list = temp_Bp_list
                NBp_list = temp_NBp_list
                UPa_divlist = temp_UPa_divlist
            i += 1
        R_data = numpy.append(R_data, attr_data[:,n, numpy.newaxis], axis=1)
        attr_data = deal_data(attr_data, n, n)
        U_list = list(set(U_list).difference(set(Bp_list + NBp_list)))
        Upos_list = list(set(Upos_list).difference(set(Bp_list)))
        Uneg_list = list(set(Uneg_list).difference(set(NBp_list)))
    print_red(my_data,R_data)

def print_red(my_data, Red_data):
    red_set = []
    for i in range(Red_data.shape[1]):
        for j in range(my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    print(red_set)

if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile()
    # x = []
    # y = []
    # for i in range(len(my_data)):
    #     if (i+1)%100 ==0:
    #         start = time.perf_counter()
    #         Reduce_basedSig(my_data[range(0, i)])
    #         end = time.perf_counter()
    #         x.append(i+1)
    #         y.append(end - start)
    # print(x,y)
    # draw(x,y);
    # end = time.perf_counter()
    # print(end - start)
    Reduce_basedSig(my_data)
    end = time.perf_counter()
    print(end - start)