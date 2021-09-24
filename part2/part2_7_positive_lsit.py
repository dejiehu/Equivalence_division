'''
基于正域 正域加速
'''
import time
import numpy
from part2.quote_file import div,deal_data,getCore_data,del_dup,data_add

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(' ')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    return  pos_list

def dependency(pos_list,my_data):#依赖度
     dep_num =  (len(pos_list) / len(my_data))
     # print("依赖度:",dep_num)
     return dep_num

def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核
    core_list = []
    for i in range(len(con_data[0])-1,-1,-1):
        temp_con_data = deal_data(con_data,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        if dep_num != dependency(pos_list,con_data):
            print("第",i+1,"个属性为核属性")
            core_list.append(i)
    print(core_list,"core_list")
    return core_list

def Red(con_data,core_list,dec_divlist):
    red_data = getCore_data(core_list, con_data)  # core_data
    temp_red_data = [red_data[i][:] for i in range(len(red_data))]
    temp_con_data = [con_data[i][:] for i in range(len(con_data))]
    dict ={}
    attr_data,attr_list = del_dup(con_data,core_list)
    while dependency(pos(dec_divlist,div(temp_red_data)),temp_con_data) != dependency(pos(dec_divlist, div(temp_con_data)), temp_con_data):
        dict.clear()
        con_key = -1  # 字典key
        con_value = 0  # 字典value
        pos_list = pos(dec_divlist,div(red_data))
        m = len(temp_con_data) - 1
        while m >= 0:
            if set(pos_list).__contains__(m):  #删除对象
                del temp_con_data[m]
                del temp_red_data[m]
                del attr_data[m]
            m -= 1
        for n in range(len(attr_data[0])):
            temp_Red_data = data_add(attr_data,temp_red_data,n)
            dict[n] = dependency(pos(dec_divlist, div(temp_Red_data)), temp_con_data)
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        temp_R = numpy.append(temp_R,   attr_data[:, con_key, numpy.newaxis], axis=1  )
        red = numpy.append(red,   temp_attr_data[:, con_key, numpy.newaxis], axis=1)
        attr_data = deal_data(attr_data,con_key,con_key)
        temp_attr_data = deal_data(temp_attr_data,con_key,con_key)
        P = div(temp_R)
    print_red(con_data,red)

def print_red(my_data,Red_data):
    red_set =[]
    for i in range(Red_data.shape[1]):
        for j in range( my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    print(red_set)


if __name__ == "__main__":
    start = time.perf_counter()
    list_data = readfileBylist("../data.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist", con_divlist)
    print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    print("pos_list",pos_list)
    dep_num = dependency(pos_list,list_data)
    print("dep_num",dep_num)
    core_data = core(con_data, dec_divlist, dep_num)
    Red(core_data,dec_divlist,con_data)
    end = time.perf_counter()
    print(end - start)