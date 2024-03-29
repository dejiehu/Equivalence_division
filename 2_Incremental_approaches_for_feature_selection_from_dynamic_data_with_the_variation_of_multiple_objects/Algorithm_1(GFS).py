import time
from itertools import chain
import numpy
'''
《多目标变化下动态数据特征选择的增量方法》
基于依赖度的属性约简   
'''

def readfile(filename):#读文件
    my_data = numpy.loadtxt(filename)
    my_data = my_data.astype(int)
    # print(my_data)
    # print("my_data.shape:",my_data.shape)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

def getCore_data(core_list,con_data):    #从所有数据中取出和属性数据
    core_data = numpy.empty(shape=(con_data.shape[0],0))
    core_data = core_data.astype(int)
    for i in core_list:
        core_data = numpy.append(core_data,con_data[:,i,numpy.newaxis],axis=1)
    return core_data

def div(my_data): #1.数据表，2、3.删除元素下表   求划分集合
    div_list =[]#返回的划分集合
    list1 = []
    for i in range(len(my_data)):  # 8行
        list1.clear()
        if list(chain.from_iterable(div_list)).__contains__(i):  # 展开
            continue
        list1.append(i)
        for j in range(i + 1, len(my_data)):
            if ((my_data[i] == my_data[j]).all()):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

# def Max_min(con_data,U_list):  #找出属性最大最小值
#     Mm_list = []
#     for i in range(con_data.shape[1]):
#         min = 10000
#         Max = 0
#         for j in U_list:
#             if con_data[j][i] > Max:
#                 Max = con_data[j][i]
#             if con_data[j][i] < min:
#                 min = con_data[j][i]
#         Mm_list.append([Max,min])
#     return Mm_list
#
# def div(my_data):    #等价类的划分
#     U_linkList = [i for i in range(len(my_data))]
#     Mm_list = Max_min(my_data,U_linkList)
#     for i in range(len(Mm_list)):
#         queue_linkList = [[]]*(Mm_list[i][0] - Mm_list[i][1] + 1)
#         for j in U_linkList:
#             queue_linkList[my_data[j][i] - Mm_list[i][1]] = queue_linkList[my_data[j][i] - Mm_list[i][1]] + [j]
#         U_linkList.clear()
#         U_linkList = list(chain.from_iterable(queue_linkList))
#     div_list = []
#     temp_list = [U_linkList[0]]
#     for i in range(1,len(U_linkList)):
#         if((my_data[U_linkList[i]] == my_data[U_linkList[i-1]]).all()):
#             temp_list.append(U_linkList[i])
#             continue
#         div_list.append(temp_list)
#         temp_list = [U_linkList[i]]
#     div_list.append(temp_list)
#     return div_list

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    return  pos_list

def dependency(pos_list,my_data):#依赖度
     dep_num =  (len(pos_list)/my_data.shape[0])
     # print("依赖度:",dep_num)
     return dep_num

def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核
    core_list = []
    for i in range(con_data.shape[1]):
        temp_con_data = deal_data(con_data,i,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        if dep_num != dependency(pos_list,con_data):
            core_list.append(i)
    print(core_list)
    return core_list

def Red(con_data,dec_divlist,core_list,dep_num):#约简
    core_data = getCore_data(core_list,con_data)
    core_dep = dependency(pos(dec_divlist,div(core_data)),con_data)
    Red_data = core_data
    att_data = con_data
    core_list = sorted(core_list,reverse=True)
    for i in core_list:
        att_data = deal_data(att_data,i,i)
    Red_dep = core_dep
    dict = {}#字典存放添加的依赖度
    num = 0
    # print(Red_dep, dep_num)
    while Red_dep != dep_num:
        # print(Red_dep, dep_num)
        num += 1
        dict.clear()
        con_key = -1#字典key
        con_value = 0#字典value
        for k in range(att_data.shape[1]):
            temp_Red_data = Red_data
            temp_Red_data = numpy.append(temp_Red_data,att_data[:,k,numpy.newaxis],axis=1)
            Red_divlist = div(temp_Red_data)
            dict[k] = dependency(pos(dec_divlist,Red_divlist),con_data) - core_dep
        # print(dict)
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        Red_data = numpy.append(Red_data,att_data[:,con_key,numpy.newaxis],axis=1)
        att_data = deal_data(att_data,con_key,con_key)
        Red_dep = dependency(pos(dec_divlist,div(Red_data)), con_data)#添加条件属性后的依赖度
        print(Red_dep)
    return Red_data

def De_redundancy(Red_data,dec_divlist,dep_num):# 去冗余
    i = 0
    while i < Red_data.shape[1]:
        temp_Red_data = deal_data(Red_data,i,i)
        dep = dependency(pos(dec_divlist, div(temp_Red_data)), Red_data)
        if dep_num == dep:
            Red_data = deal_data(Red_data,i,i)
            i = 0
            continue
        i += 1
    return Red_data

def print_red(my_data,Red_data):
    red_set =[]
    for i in range(Red_data.shape[1]):
        for j in range( my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    print(red_set)

if __name__ == "__main__":

    my_data = readfile("../complete_dataSet_classication/german.txt")
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    start = time.perf_counter()
    con_divlist = div(con_data)
    end = time.perf_counter()
    print(end - start)
    dec_divlist = div(dec_data)
    pos_list = pos(dec_divlist,con_divlist)
    dep_num = dependency(pos_list,my_data)
    core_list = core(con_data, dec_divlist,dep_num)
    Red_data = Red(con_data,dec_divlist,core_list,dep_num)
    # print_red(my_data, De_redundancy(Red_data,dec_divlist,dep_num))
    # end = time.perf_counter()
    print(end - start)