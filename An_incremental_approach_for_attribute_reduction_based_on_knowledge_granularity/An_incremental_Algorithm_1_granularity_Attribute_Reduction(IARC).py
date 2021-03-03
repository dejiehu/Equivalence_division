import math
from itertools import chain
import numpy
'''
基于知识粒的增量式属性约简
'''

def readfile(file):     #读文件
    my_data = numpy.loadtxt(file)
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

def div(my_data):    #等价类的划分
    U_linkList = [i for i in range(len(my_data))]
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

def granularity(con_divlist): #知识粒
    GP = 0
    U = len(list(chain.from_iterable(con_divlist)))
    for i in con_divlist:
        GP = math.pow(len(i),2)/math.pow(U,2) +GP
    print(GP,"gp")
    return GP

def condition_granularity(dec_data,con_data):  #相对条件粒计算
    return granularity(div(con_data)) - granularity(div(numpy.append(con_data,dec_data,axis=1)))

def U_Ux_condition_granularity(U_dec_data,Ux_dec_data,U_con_data,Ux_con_data):  #相对条件粒计算
    Ck, Csum, CU_Ux_divlist = merge_divlist(div(U_con_data).copy(), Add_Ux_dataShape(U_data, div(Ux_con_data)).copy(), U_con_data, Ux_con_data)
    Ck, C_D_sum, CU_Ux_divlist = merge_divlist(div(numpy.append(U_con_data,U_dec_data,axis=1)).copy(),Add_Ux_dataShape(U_data, div(numpy.append(Ux_con_data,Ux_dec_data,axis=1))).copy(),numpy.append(U_con_data,U_dec_data,axis=1), numpy.append(Ux_con_data,Ux_dec_data,axis=1))
    return (math.pow(len(U_con_data),2) * condition_granularity(U_dec_data,U_con_data) + math.pow(len(Ux_con_data),2) * condition_granularity(Ux_dec_data,Ux_con_data) + 2 * Csum - 2 * C_D_sum)/math.pow((U_con_data.shape[0] + Ux_con_data.shape[0]),2)

# def Core(dec_data,con_data):  #求核
#     core_data = numpy.empty(shape=(len(con_data), 0))
#     core_data = core_data.astype(int)
#     core = []
#     for i in range(con_data.shape[1]):
#         temp_core_data = deal_data(con_data,i,i)
#         if condition_granularity(dec_data,temp_core_data) - condition_granularity(dec_data,con_data) != 0:
#             core_data = numpy.append(core_data, con_data[:, i, numpy.newaxis], axis=1)
#             core += [i]
#     # print(core)
#     return core_data,core

def red(U_dec_data, U_con_data,Ux_dec_data,Ux_con_data,Ux_red_data):# 求约简
    if condition_granularity(Ux_dec_data, Ux_con_data) == condition_granularity(Ux_dec_data, Ux_red_data):
        return
    else:
        print(U_Ux_condition_granularity(U_dec_data,Ux_dec_data,U_con_data,Ux_con_data))

    # red_data,red_num = Core(dec_data,con_data)
    # if len(red_num) == 0:
    #     print("无约简")
    #     return
    # attr_data = numpy.empty(shape=(len(con_data), 0))
    # attr_data = attr_data.astype(int)
    # attr_num = []
    # for i in range(con_data.shape[1]):
    #     if not(red_num.__contains__(i)):
    #         attr_data = numpy.append(attr_data, con_data[:, i, numpy.newaxis], axis=1)
    #         attr_num += [i]
    # while condition_granularity(dec_data,con_data) != condition_granularity(dec_data,red_data):
    #     dict = {}
    #     con_key = -1  # 字典key
    #     con_value = -1  # 字典value
    #     for i in range(attr_data.shape[1]):
    #         temp_red_data = red_data
    #         temp_red_data = numpy.append(temp_red_data, attr_data[:, i, numpy.newaxis], axis=1)
    #         dict[i] = condition_granularity(dec_data,red_data) - condition_granularity(dec_data,temp_red_data)
    #     print(dict)
    #     for key in dict:
    #         if dict[key] > con_value:
    #             con_value = dict[key]
    #             con_key = key
    #     red_data = numpy.append(red_data,attr_data[:,con_key,numpy.newaxis],axis=1)
    #     red_num += [attr_num[con_key]]
    #     attr_data = deal_data(attr_data, con_key, con_key)
    #     del attr_num[con_key]
    # return red_data,red_num

def De_redundancy(red_data,red_num,dec_data,con_data):# 去冗余
    i = 0
    while i < red_data.shape[1]:
        temp_Red_data = red_data
        temp_Red_data = deal_data(temp_Red_data,i,i)
        if condition_granularity(dec_data,con_data) == condition_granularity(dec_data,temp_Red_data):
            red_data = deal_data(red_data,i,i)
            del red_num[i]
            i = 0
            continue
        i += 1
    print(red_data)
    print(red_num)
    return red_data,red_num

def Add_Ux_dataShape(U_data,Ux_divlist):   #  调整增加的属性的对象序号
    for i in range(len(Ux_divlist)):
        for j in range(len(Ux_divlist[i])):
            Ux_divlist[i][j] += U_data.shape[0]
    return Ux_divlist

def cal_red_divlist(red_num,con_data):   #根据核属性数值计算核属性数据
    red_data = numpy.empty(shape=(len(con_data), 0))
    red_data = red_data.astype(int)
    for i in red_num:
        red_data =  numpy.append(red_data,con_data[:,i,numpy.newaxis],axis=1)
    return red_data

def merge_divlist(U_divlist,Ux_divlist,U_data,Ux_data):#      U/C + Ux/C
    U_Ux_divlist = []
    sum = 0
    for i in range(len(Ux_divlist)-1,-1,-1):
        for j in range(len(U_divlist)-1,-1,-1):
            if (U_data[U_divlist[j][0]] == Ux_data[(Ux_divlist[i][0]) - U_data.shape[0]]).all():
                U_Ux_divlist.append(U_divlist[j] + Ux_divlist[i])
                sum += len(U_divlist[j]) * len(Ux_divlist[i])
                del U_divlist[j],Ux_divlist[i]
                break
    k = len(U_Ux_divlist)
    U_Ux_divlist.append(U_divlist + Ux_divlist)
    return k,sum,U_Ux_divlist


if __name__ == '__main__':
    U_data = readfile('table_1.txt')
    RED = [1, 4]
    Ux_data = readfile('incremental.txt')
    U_Ux_data = numpy.append(U_data,Ux_data,axis=0)
    U_con_data = deal_data(U_data, U_data.shape[1] - 1, U_data.shape[1] - 1)
    U_dec_data = deal_data(U_data, 0, U_data.shape[1] - 2)
    U_con_divlist = div(U_con_data)

    U_dec_divlist = div(U_dec_data)
    Ux_con_data = deal_data(Ux_data, Ux_data.shape[1] - 1, Ux_data.shape[1] - 1)
    Ux_dec_data = deal_data(Ux_data, 0, Ux_data.shape[1] - 2)
    Ux_con_divlist = Add_Ux_dataShape(U_data, div(Ux_con_data))

    Ux_dec_divlist = div(Ux_dec_data)
    U_red_data = cal_red_divlist(RED,U_con_data)
    Ux_red_data = cal_red_divlist(RED,Ux_con_data)
    U_red_divlist = div(U_red_data)
    Ux_red_divlist = Add_Ux_dataShape(U_red_data, div(Ux_red_data))
    Ck,sum,CU_Ux_divlist = merge_divlist(U_con_divlist.copy(), Ux_con_divlist.copy(), U_con_data, Ux_con_data)
    # REDk,RED_U_Ux_divlist = merge_divlist(U_red_divlist.copy(), Ux_red_divlist.copy(), U_red_data, Ux_red_data)
    red(U_dec_data, U_con_data, Ux_dec_data, Ux_con_data,Ux_red_data)
    # red_data,red_num = red(dec_data, con_data)
    # red_data,red_num = De_redundancy(red_data, red_num, dec_data, con_data)


    U_divlist = div(U_data)
    Ux_divlist = Add_Ux_dataShape(U_data, div(Ux_data))
    k, sum, U_Ux_divlist = merge_divlist(U_divlist.copy(), Ux_divlist.copy(), U_data, Ux_data)
    print(U_divlist,k)
    print(Ux_divlist, k)
    print(U_Ux_divlist, k)