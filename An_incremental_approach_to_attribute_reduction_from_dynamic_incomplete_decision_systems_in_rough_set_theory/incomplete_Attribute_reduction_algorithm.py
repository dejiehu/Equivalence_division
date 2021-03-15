import time
from itertools import chain
import numpy

def readfile():#读文件
    my_data = []
    f = open("../incomplete_table.txt", "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    for i in range(0, lines.__len__(), 1):  # (开始/左边界, 结束/右边界, 步长)
        list = []  ## 空列表, 将第i行数据存入list中
        for word in lines[i].split():
            word = word.strip()
            list.append(word)
        my_data.append(list)
    print(my_data)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    data = [my_data[i][:] for i in range(len(my_data))]
    if n + 1 > m:
        for d in range(n,m-1,-1):
            for i in range(len(data)):
                del data[i][d]
    return data

def getCore_data(core_list,con_data):    #从所有数据中取出和属性数据
    core_data = numpy.empty(shape=(con_data.shape[0],0))
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
            if (my_data[i] == my_data[j]):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

def get_matrix(my_data): #
    U_list = {i for i in range(len(my_data))}
    Sp_matrix = [[] for i in range(len(my_data))]
    for i in range(len(my_data)):
        for j in range(len(my_data[0])):
            sp_set = set()
            index = 1
            for k in range(len(my_data)):
                if my_data[i][j] == '*':
                    Sp_matrix[i].append(U_list)
                    index = 0
                    break
                if my_data[i][j] == my_data[k][j] or my_data[k][j] == '*':
                    sp_set.add(k)
            if index == 1:
                Sp_matrix[i].append(sp_set.copy())
    return Sp_matrix

def div_base_matric(Sp_matrix,dec_data,con_list):
    dec_divlist = div(dec_data)
    print(dec_divlist)


def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if j.issubset(i):
                pos_list += j
    return  pos_list

# def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核
#     core_list = []
#     for i in range(con_data.shape[1]):
#         temp_con_data = deal_data(con_data,i,i)
#         temp_con_divlist = div(temp_con_data)
#         pos_list = pos(dec_divlist, temp_con_divlist)
#         if dep_num != dependency(pos_list,con_data):
#             print("第",i,"个属性为核属性")
#             core_list.append(i)
#     print(core_list)
#     return core_list

if __name__ == "__main__":
    start = time.perf_counter()
    my_data = readfile()
    con_data = deal_data(my_data, len(my_data[0]) - 1, len(my_data[0]) - 1)
    dec_data = deal_data(my_data, 0, len(my_data[0])  - 2)
    Sp_matrix = get_matrix(con_data)
    print(Sp_matrix)
    con_list = [i for i in range(len(con_data[0]))]
    div_base_matric(Sp_matrix, dec_data, con_list)

    # con_divlist = div(con_data)
    # pos_list = pos(dec_divlist,con_divlist)
    # dep_num = dependency(pos_list,my_data)
    # core_list = core(con_data, dec_divlist,dep_num)
    # Red_data = Red(con_data,dec_divlist,core_list,dep_num)
    # print_red(my_data, De_redundancy(Red_data,dec_divlist,dep_num))
    # end = time.perf_counter()
    # print(end - start)

    # def Red(con_data,dec_divlist,core_list,dep_num):#约简
    #     core_data = getCore_data(core_list,con_data)
    #     core_dep = dependency(pos(dec_divlist,div(core_data)),con_data)
    #     Red_data = core_data
    #     att_data = con_data
    #     core_list = sorted(core_list,reverse=True)
    #     for i in core_list:
    #         att_data = deal_data(att_data,i,i)
    #     Red_dep = core_dep
    #     dict = {}#字典存放添加的依赖度
    #     num = 0
    #     print(Red_dep, dep_num)
    #     while Red_dep != dep_num:
    #         print(Red_dep, dep_num)
    #         print("第",num,"次循环了")
    #         num += 1
    #         dict.clear()
    #         con_key = -1#字典key
    #         con_value = 0#字典value
    #         for k in range(att_data.shape[1]):
    #             temp_Red_data = Red_data
    #             temp_Red_data = numpy.append(temp_Red_data,att_data[:,k,numpy.newaxis],axis=1)
    #             Red_divlist = div(temp_Red_data)
    #             dict[k] = dependency(pos(dec_divlist,Red_divlist),con_data) - core_dep
    #         print(dict)
    #         for key in dict:
    #             if con_value < dict[key]:
    #                 con_value = dict[key]
    #                 con_key = key
    #         Red_data = numpy.append(Red_data,att_data[:,con_key,numpy.newaxis],axis=1)
    #         att_data = deal_data(att_data,con_key,con_key)
    #         Red_dep = dependency(pos(dec_divlist,div(Red_data)), con_data)#添加条件属性后的依赖度
    #         print(Red_dep)
    #     return Red_data
    #
    # def De_redundancy(Red_data,dec_divlist,dep_num):# 去冗余
    #     i = 0
    #     while i < Red_data.shape[1]:
    #         temp_Red_data = deal_data(Red_data,i,i)
    #         dep = dependency(pos(dec_divlist, div(temp_Red_data)), Red_data)
    #         if dep_num == dep:
    #             Red_data = deal_data(Red_data,i,i)
    #             i = 0
    #             continue
    #         i += 1
    #     return Red_data
    #
    # def print_red(my_data,Red_data):
    #     red_set =[]
    #     for i in range(Red_data.shape[1]):
    #         for j in range( my_data.shape[1]):
    #             if (my_data[:, j] == Red_data[:, i]).all():
    #                 red_set.append(j)
    #     print(red_set)