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

def div_base_matric(Sp_matrix,con_list,del_list):
    con_list = list(set(con_list) - set(del_list))
    sp_list = []
    for j in range(len(Sp_matrix)):
        sp = set(k for k in range(len(dec_data)))
        for i in con_list:
            sp = sp & Sp_matrix[j][i]
        sp_list.append(list(sp.copy()))
    return sp_list

def pos(dec_divlist,sp_divlist):  #子集  正域集合
    pos_list=[]
    for i in range(len(dec_divlist)):
         for j in range(len(sp_divlist)):
            if set(sp_divlist[j]).issubset(dec_divlist[i]):
                pos_list += [j]
    return pos_list

def core(Sp_matrix,con_list,dec_divlist):# 根据 属性重要度  求核
    core_list = []
    pos_c = pos(dec_divlist,div_base_matric(Sp_matrix,con_list,[]))
    for i in con_list:
        if len(set(pos_c) - set(pos(dec_divlist,div_base_matric(Sp_matrix,con_list,[i])))) > 0:
            core_list.append(i)
    print(core_list)
    return core_list

def red(Sp_matrix,con_list,dec_divlist,core_list):
    red_list = core_list.copy()
    pos_c = pos(dec_divlist, div_base_matric(Sp_matrix, con_list, []))
    attr_list = list(set(con_list) - set(red_list))
    while pos_c != pos(dec_divlist,div_base_matric(Sp_matrix,red_list,[])):
        print("111111")
        dict = {}
        con_key = -1  # 字典key
        con_value = -1  # 字典value
        for i in attr_list:
            dict[i] = len(set(pos(dec_divlist, div_base_matric(Sp_matrix, red_list + [i], []))) - set(pos(dec_divlist,div_base_matric(Sp_matrix,core_list,[]))))
        for key in dict:
            if dict[key] > con_value:
                con_value = dict[key]
                con_key = key
        attr_list.remove(con_key)
        red_list += [con_key]
    print(red_list)
    return red_list

if __name__ == "__main__":
    start = time.perf_counter()
    my_data = readfile()
    con_data = deal_data(my_data, len(my_data[0]) - 1, len(my_data[0]) - 1)
    dec_data = deal_data(my_data, 0, len(my_data[0])  - 2)
    Sp_matrix = get_matrix(con_data)
    con_list = [i for i in range(len(con_data[0]))]
    dec_divlist = div(dec_data)
    core_list = core(Sp_matrix, con_list, dec_divlist)
    red(Sp_matrix, con_list, dec_divlist, core_list)