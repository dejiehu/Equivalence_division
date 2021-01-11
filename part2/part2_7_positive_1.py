'''
基于正域 正域加速
'''
import time
import numpy

def readfile():#读文件
    my_data = numpy.loadtxt('..\zoo.txt')
    print(my_data)
    print("my_data.shape:",my_data.shape)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

def div(my_data): #1.数据表，2、3.删除元素下表   求划分集合
    divlist =[]#返回的划分集合
    list = []
    jump = 1
    for i in range(len(my_data)):  #
        list.clear()
        for l in range(len(divlist)):
            if (divlist[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list.append(i)
        for j in range(i + 1, len(my_data)):
            if ((my_data[i] == my_data[j]).all()):
                list.append(j)
        divlist.append(list.copy())
    return divlist

def divByUi(my_data,Ui): #1.数据表，2、3.删除元素下表   求划分集合
    divlist =[]#返回的划分集合
    list = []
    jump = 1
    for i in Ui:  # 8行
        list.clear()
        for l in range(len(divlist)):
            if (divlist[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list.append(i)
        for j in Ui:
            if j == i:
                continue
            if ((my_data[i] == my_data[j]).all()):
                list.append(j)
        divlist.append(list.copy())
    return divlist

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    return  pos_list

def dependency(pos_list,my_data):#依赖度
     dep_num =  (len(pos_list)/len(my_data))
     return dep_num

def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核
    core_data = numpy.empty(shape=(con_data.shape[0],0))
    for i in range(con_data.shape[1]):
        temp_con_data = deal_data(con_data,i,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        # if dependency(pos(dec_divlist, div(con_data)), con_data) != dependency(pos_list, con_data):
        if dep_num != dependency(pos_list,con_data):
            print("第",i,"个属性为核属性")
            core_data = numpy.append(core_data,con_data[:,i,numpy.newaxis],axis=1)
    # print(core_data)
    return core_data

def Red(core_data,dec_divlist,con_data):
    red = core_data
    U = [i for i in range(con_data.shape[0])]
    Ui = U
    dict ={}
    attr_data = con_data
    k = 0
    j = 0
    while k < core_data.shape[1]:#C-red
        while j < attr_data.shape[1]:
            if (core_data[:, k] == attr_data[:, j]).all():
                attr_data = deal_data(attr_data, j, j)
                continue
            j += 1
        k += 1
    # print("U",Ui)
    while dependency(pos(dec_divlist,divByUi(red,Ui)),Ui) != dependency(pos(dec_divlist, divByUi(con_data,Ui)), Ui):
        dict.clear()
        con_key = -1  # 字典key
        con_value = 0  # 字典value
        pos_list = pos(dec_divlist,div(red))
        # print("决策属性划分",dec_divlist)
        # print("条件属性划分", div(red))
        m = len(Ui)-1
        while m >= 0:
            if set(pos_list).__contains__(Ui[m]):  #删除对象
                del Ui[m]
            m -= 1
        # print("正域",pos_list)
        # print("Ui",Ui)
        for n in range(attr_data.shape[1]):
            temp_Red_data = red
            temp_Red_data = numpy.append(temp_Red_data, attr_data[:, n, numpy.newaxis], axis=1)
            dict[n] = dependency(pos(dec_divlist, divByUi(temp_Red_data,Ui)), Ui)
            # print(dependency(pos(dec_divlist, divByUi(temp_Red_data,Ui)), Ui) , dependency(pos(dec_divlist, divByUi(red,Ui)), Ui))
        # print(dict)
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        red = numpy.append(red, attr_data[:, con_key, numpy.newaxis], axis=1)
        attr_data = deal_data(attr_data,con_key,con_key)
    print_red(con_data,red)

def print_red(my_data,Red_data):
    red_set =[]
    for i in range(Red_data.shape[1]):
        for j in range( my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    print("约简：",red_set)


if __name__ == "__main__":
    start = time.perf_counter()
    my_data = readfile()
    con_data = deal_data(my_data, my_data.shape[1]-1, my_data.shape[1]-1)
    dec_data = deal_data(my_data, 0, my_data.shape[1]-2)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist", con_divlist)
    print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    print("pos_list",pos_list)
    dep_num = dependency(pos_list,my_data)
    print("dep_num",dep_num)
    core_data = core(con_data, dec_divlist,dep_num)
    # print(dependency(pos(dec_divlist,div(core_data)),con_data))
    Red(core_data,dec_divlist,con_data)
    end = time.perf_counter()
    print(end - start)