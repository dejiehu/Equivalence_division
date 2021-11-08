'''
基于正域 正域加速
'''
import time
from itertools import chain

from part2.quote_file import deal_data,getCore_data,del_dup,data_add

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data

def Max_min(con_data,U_list):  #找出属性最大最小值
    Mm_list = []
    for i in range(len(con_data[0])):
        min = 10000
        Max = -10000
        for j in U_list:
            if con_data[j][i] > Max:
                Max = con_data[j][i]
                continue
            if con_data[j][i] < min:
                min = con_data[j][i]
        Mm_list.append([Max,min])
    return Mm_list

# def Max_min(con_data,U_list):  #找出属性最大最小值
#     Mm_list = []
#     temp_con_data  = [con_data[i][:] for i in range(len(con_data))]
#     temp_con_data = list(map(list, zip(*temp_con_data)))
#     for i in temp_con_data:
#         Mm_list.append([max(i),min(i)])
#     return Mm_list

def div(my_data):    #等价类的划分
    U_linkList =  [i for i in range(len(my_data))]
    U_List = U_linkList.copy()
    for i in range(len(my_data[0])):
        min = 10000
        Max = -10000
        for j in U_List:
            if my_data[j][i] > Max:
                Max = my_data[j][i]
                continue
            if my_data[j][i] < min:
                min = con_data[j][i]

        queue_linkList = [[]]*(Max - min + 1)
        for j in U_linkList:
            index = my_data[j][i] - min
            queue_linkList[index] = queue_linkList[index] + [j]
        U_linkList.clear()
        U_linkList = list(chain.from_iterable(queue_linkList))
    div_list = []
    temp_list = [U_linkList[0]]
    for i in range(1,len(U_linkList)):
        if((my_data[U_linkList[i]] == my_data[U_linkList[i-1]])):
            temp_list.append(U_linkList[i])
            continue
        div_list.append(temp_list)
        temp_list = [U_linkList[i]]
    div_list.append(temp_list)
    return div_list

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    temp_con_divlist = [con_divlist[i][:] for i in range(len(con_divlist))]
    for i in dec_divlist:
         for j in range(len(temp_con_divlist)-1,-1,-1):
            if set(temp_con_divlist[j]).issubset(i):
                pos_list += temp_con_divlist[j]
                del temp_con_divlist[j]
    return  pos_list

# def pos(dec_divlist,con_divlist):  #子集  正域集合
#     pos_list=[]
#     for i in dec_divlist:
#          for j in con_divlist:
#             if set(j).issubset(i):
#                 pos_list +=j
#     return  pos_list

def dependency(pos_list,my_data):#依赖度
     dep_num =  (len(pos_list) / len(my_data))
     # print("依赖度:",dep_num)
     return dep_num

def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核

    core_list = []
    for i in range(len(con_data[0])-1,-1,-1):
        start = time.perf_counter()
        temp_con_data = deal_data(con_data,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        if dep_num != dependency(pos_list,con_data):
            print("第",i,"个属性为核属性")
            core_list.append(i)
        end = time.perf_counter()
        print(end - start)
    print(core_list,"core_list")

    return core_list

def Red(con_data,core_list,dec_data):
    start = time.perf_counter()
    red_data = getCore_data(core_list, con_data)  # core_data
    red_list = core_list.copy()
    temp_red_data = [red_data[i][:] for i in range(len(red_data))]
    temp_con_data = [con_data[i][:] for i in range(len(con_data))]
    temp_dec_data = [dec_data[i][:] for i in range(len(dec_data))]
    dict ={}
    attr_data,attr_list = del_dup(con_data,core_list)
    end = time.perf_counter()
    print(end - start)
    while dependency(pos(div(temp_dec_data),div(temp_red_data)),temp_con_data) != dependency(pos(div(temp_dec_data), div(temp_con_data)), temp_con_data):
        dict.clear()
        print("1")
        con_key = -1  # 字典key
        con_value = -10000  # 字典value
        pos_list = pos(div(dec_data),div(red_data))
        m = len(con_data) - 1
        temp_red_data = [red_data[i][:] for i in range(len(red_data))]
        temp_con_data = [con_data[i][:] for i in range(len(con_data))]
        temp_attr_data = [attr_data[i][:] for i in range(len(attr_data))]
        temp_dec_data = [dec_data[i][:] for i in range(len(dec_data))]
        while m >= 0:
            if set(pos_list).__contains__(m):  # 删除对象
                del temp_con_data[m]
                del temp_red_data[m]
                del temp_attr_data[m]
                del temp_dec_data[m]  #删掉后样本的序号会改变，所有决策也要删除
            m -= 1
        for n in range(len(attr_data[0])):
            dict[n] = dependency(pos(div(temp_dec_data), div(data_add(temp_attr_data,temp_red_data,n))), temp_con_data)
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        temp_red_data = data_add(temp_attr_data,temp_red_data,con_key)
        red_data = data_add(attr_data,red_data,con_key)
        attr_data = deal_data(attr_data,con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
    print(red_list)


if __name__ == "__main__":
    start = time.perf_counter()
    list_data = readfileBylist("../zoo.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    # print("con_divlist", con_divlist)
    # print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    dep_num = dependency(pos_list,list_data)
    print("dep_num",dep_num)
    end1 = time.perf_counter()
    print(end1 - start)
    core_list = core(con_data, dec_divlist, dep_num)
    end2 = time.perf_counter()
    print(end2-start)
    Red(con_data,core_list,dec_data)
    end = time.perf_counter()
    print(end - start)