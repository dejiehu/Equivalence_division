import time
from itertools import chain
import numpy

def readfile(file_name):#读文件
    my_data = []
    f = open(file_name, "r", encoding='utf-8')
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

def get_new_matrix(Sp_matrix,em_list):
    new_sp_matrix = [Sp_matrix[i][:] for i in range(len(Sp_matrix))]
    for i in em_list:
        # print(i)
        for j in range(len(new_sp_matrix[i])):
            # print(new_sp_matrix[i][j])
            for k in new_sp_matrix[i][j]:
                # print(k)
                new_sp_matrix[k][j] = new_sp_matrix[k][j] - {i}
    return new_sp_matrix

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

def new_pos(new_sp_matrix,red_list,dec_divlist,em_list):
    sp_divlist = div_base_matric(new_sp_matrix, red_list, [])
    list1 = []
    for i in em_list:
        for j in sp_divlist[i]:
            if issubset_dec(dec_divlist,sp_divlist[j]) == 1:
               list1.append(j)
    return set(pos(dec_divlist,sp_divlist)) - set(em_list) | set(list1)

def issubset_dec(dec_list,con_list):
    for i in dec_list:
        if set(con_list).issubset(i):
            return 1
    return 0

def red(Sp_matrix,con_list,dec_divlist,red_list,em_list):
    new_sp_matrix = get_new_matrix(Sp_matrix, em_list)
    pos_c = new_pos(new_sp_matrix, con_list, dec_divlist, em_list)
    i = len(red_list) - 1
    while i >= 0:
        if pos_c  == new_pos(new_sp_matrix, set(red_list) - {red_list[i]}, dec_divlist, em_list):
            del red_list[i]
        i = i - 1
    print(red_list)

if __name__ == "__main__":
    start = time.perf_counter()
    my_data = readfile("incomplete_table.txt")
    red_list = [2,3]
    em_list =[1]
    con_data = deal_data(my_data, len(my_data[0]) - 1, len(my_data[0]) - 1)
    dec_data = deal_data(my_data, 0, len(my_data[0])  - 2)
    Sp_matrix = get_matrix(con_data)
    con_list = [i for i in range(len(con_data[0]))]
    dec_divlist = div(dec_data)
    red(Sp_matrix,con_list,dec_divlist,red_list,em_list)
    end = time.perf_counter()
    print(end - start)