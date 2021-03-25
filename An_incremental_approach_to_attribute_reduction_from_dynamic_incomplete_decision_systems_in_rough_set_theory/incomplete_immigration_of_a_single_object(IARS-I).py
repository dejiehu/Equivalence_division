import time
from itertools import chain
import numpy

def readfile(file_name):#读文件
    U_con_data = []
    f = open(file_name, "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    for i in range(0, lines.__len__(), 1):  # (开始/左边界, 结束/右边界, 步长)
        list = []  ## 空列表, 将第i行数据存入list中
        for word in lines[i].split():
            word = word.strip()
            list.append(word)
        U_con_data.append(list)
    print(U_con_data)
    return U_con_data

def deal_data(U_con_data,m,n):#处理数据表
    data = [U_con_data[i][:] for i in range(len(U_con_data))]
    if n + 1 > m:
        for d in range(n,m-1,-1):
            for i in range(len(data)):
                del data[i][d]
    return data

def div(U_con_data): #1.数据表，2、3.删除元素下表   求划分集合
    div_list =[]#返回的划分集合
    list1 = []
    for i in range(len(U_con_data)):  # 8行
        list1.clear()
        if list(chain.from_iterable(div_list)).__contains__(i):  # 展开
            continue
        list1.append(i)
        for j in range(i + 1, len(U_con_data)):
            if (U_con_data[i] == U_con_data[j]):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

def get_matrix(U_con_data):  # 获取相容关系矩阵
    U_list = {i for i in range(len(U_con_data))}
    U_sp_matrix = [[] for i in range(len(U_con_data))]
    for i in range(len(U_con_data)):
        for j in range(len(U_con_data[0])):
            sp_set = set()
            index = 1
            for k in range(len(U_con_data)):
                if U_con_data[i][j] == '*':
                    U_sp_matrix[i].append(U_list)
                    index = 0
                    break
                if U_con_data[i][j] == U_con_data[k][j] or U_con_data[k][j] == '*':
                    sp_set.add(k)
            if index == 1:
                U_sp_matrix[i].append(sp_set.copy())
    return U_sp_matrix

def get_new_matrix(U_con_data,Ux_con_data,U_sp_matrix):  #根据新增数据，获取新的相容关系矩阵
    U_list = {(i + len(U_con_data)) for i in range(len(Ux_con_data))}
    U_Ux_sp_matrix = [[] for i in range(len(Ux_con_data))]
    for i in range(len(Ux_con_data)):
        for j in range(len(Ux_con_data[0])):
            sp_set = set()
            index = 1
            for k in range(len(U_con_data + Ux_con_data)):
                if Ux_con_data[i][j] == '*':
                    U_Ux_sp_matrix[i].append(U_list)
                    index = 0
                    break
                if Ux_con_data[i][j] == (U_con_data + Ux_con_data)[k][j] or (U_con_data + Ux_con_data)[k][j] == '*':
                    sp_set.add(k)
            if index == 1:
                U_Ux_sp_matrix[i].append(sp_set.copy())
    U_Ux_sp_matrix = U_sp_matrix + U_Ux_sp_matrix
    print(U_Ux_sp_matrix)
    for i in range(len(U_con_data), len(U_con_data + Ux_con_data)):
        for k in range(len(U_Ux_sp_matrix[i])):
            for j in U_Ux_sp_matrix[i][k]:
                U_Ux_sp_matrix[j][k].add(i)
    # print(U_Ux_sp_matrix)
    return U_Ux_sp_matrix

def div_base_matric(U_sp_matrix,con_list,del_list):  #根据矩阵获取相容类
    con_list = list(set(con_list) - set(del_list))
    sp_list = []
    for j in range(len(U_sp_matrix)):
        sp = set(k for k in range(len(U_sp_matrix)))
        for i in con_list:
            sp = sp & U_sp_matrix[j][i]
        sp_list.append(list(sp.copy()))
    return sp_list

def pos(dec_divlist,sp_divlist):  #子集  正域集合
    pos_list=[]
    for i in range(len(dec_divlist)):
         for j in range(len(sp_divlist)):
            if set(sp_divlist[j]).issubset(dec_divlist[i]):
                pos_list += [j]
    return pos_list

def new_pos(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,red_list,U_con_data,Ux_con_data):
    list1 = []
    list2 = []
    new_sp_list = div_base_matric(U_Ux_sp_matrix, red_list, [])
    for i in range(len(U_con_data), len(U_con_data + Ux_con_data)):
        for k in U_Ux_dec_divlist:
            if set(new_sp_list[i]).issubset(k):
                list1 +=[i]
        for j in new_sp_list[i]:
            if issubset_dec(U_Ux_dec_divlist, new_sp_list[j]) == 0:
                list2 +=[j]
    return (set(pos(dec_divlist, div_base_matric(U_sp_matrix, red_list, []))) | set(list1) - set(list2))

def issubset_dec(dec_list,con_list):
    for i in dec_list:
        if set(con_list).issubset(i):
            return 1
    return 0

def red(U_sp_matrix,U_Ux_sp_matrix,con_list,dec_divlist,U_Ux_dec_divlist,red_num,U_con_data,Ux_con_data):
    red_list = red_num.copy()
    print(div_base_matric(U_Ux_sp_matrix,con_list,[]),len(U_con_data + Ux_con_data ) - 1)
    if len(div_base_matric(U_Ux_sp_matrix,con_list,[])[len(U_con_data + Ux_con_data)-1]) == 1 & issubset_dec(
            U_Ux_dec_divlist,div_base_matric(U_Ux_sp_matrix,red_list,[])[len(U_con_data + Ux_con_data)-1]) == 1:
        print("输出了")
        return red_num
    attr_list = list(set(con_list) - set(red_list))
    dict = {}
    print(div_base_matric(U_Ux_sp_matrix,red_list,[]))
    for i in attr_list:
        dict[i] = len((new_pos(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,red_list + [i],U_con_data,Ux_con_data)) -
                      (new_pos(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,red_list,U_con_data,Ux_con_data)))
    dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    pos_c = new_pos(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,con_list,U_con_data,Ux_con_data)
    print(pos_c,new_pos(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,red_list,U_con_data,Ux_con_data))
    while pos_c != new_pos(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,red_list,U_con_data,Ux_con_data):
        red_list = red_list + [attr_list[dict[0][0]]]
        del dict[0]
    De_redundancy(U_sp_matrix, U_Ux_sp_matrix, dec_divlist, U_Ux_dec_divlist, red_num, U_con_data, Ux_con_data,
                  pos_c)

def De_redundancy(U_sp_matrix,U_Ux_sp_matrix,dec_divlist,U_Ux_dec_divlist,red_num,U_con_data,Ux_con_data,pos_c):
    i =  len(red_num) - 1
    while i >= 0:
        if pos_c == new_pos(U_sp_matrix, U_Ux_sp_matrix, dec_divlist, U_Ux_dec_divlist, set(red_num) - {red_num[i]}, U_con_data, Ux_con_data):
            del red_num[i]
        i = i - 1
    print(red_num)

if __name__ == "__main__":
    start = time.perf_counter()
    U_con_data = readfile("incomplete_table.txt")
    single_data = readfile("immigrate_singal.txt")
    red_num = [2,3]
    U_con_data = deal_data(U_con_data, len(U_con_data[0]) - 1, len(U_con_data[0]) - 1)
    dec_data = deal_data(U_con_data, 0, len(U_con_data[0])  - 2)
    Ux_con_data = deal_data(single_data, len(single_data[0]) - 1, len(single_data[0]) - 1)
    Ux_dec_data = deal_data(single_data, 0, len(single_data[0]) - 2)
    U_sp_matrix = get_matrix(U_con_data)
    con_list = [i for i in range(len(U_con_data[0]))]
    dec_divlist = div(dec_data)
    U_Ux_dec_divlist = div(dec_data + Ux_dec_data)
    print(U_sp_matrix,"111111")
    U_Ux_sp_matrix = get_new_matrix(U_con_data, Ux_con_data, U_sp_matrix)
    print(U_Ux_sp_matrix,"111111")
    red(U_sp_matrix,U_Ux_sp_matrix,con_list,dec_divlist,U_Ux_dec_divlist,red_num,U_con_data,Ux_con_data)
    end = time.perf_counter()
    print(end - start)