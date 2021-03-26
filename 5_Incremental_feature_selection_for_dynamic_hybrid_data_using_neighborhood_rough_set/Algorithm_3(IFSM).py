import copy
import math
import time
from itertools import chain

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

def deal_data(my_data,m,n):#   划分条件属性和决策属性
    data = [my_data[i][:] for i in range(len(my_data))]
    if n + 1 > m:
        for d in range(n,m-1,-1):
            for i in range(len(data)):
                del data[i][d]
    return data

def div(my_data): #等价类划分
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

def get_matrix(con_data): # 求相容关系矩阵
    U_list = {i for i in range(len(con_data))}
    U_sp_matrix = [[] for i in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(len(con_data[0])):
            sp_set = set()
            if con_data[i][j] == '*':
                U_sp_matrix[i].append(U_list)
                continue
            if j == 0 or j == 3:
                for k in range(len(con_data)):
                    if con_data[k][j] == '*' or abs(float(con_data[i][j]) - float(con_data[k][j])) <= 0.2:
                        sp_set.add(k)
                U_sp_matrix[i].append(sp_set.copy())
            if j == 1 or j == 2:
                for k in range(len(con_data)):
                    if con_data[i][j] == con_data[k][j] or con_data[k][j] == '*':
                        sp_set.add(k)
                U_sp_matrix[i].append(sp_set.copy())
    return U_sp_matrix

def get_new_matrix(U_con_data,Ux_con_data,U_sp_matrix):  #根据新增数据，获取新的相容关系矩阵
    Ux_list = {i for i in range(len(U_con_data + Ux_con_data))}
    U_Ux_sp_matrix = [[] for i in range(len(Ux_con_data))]
    for i in range(len(Ux_con_data)):
        for j in range(len(Ux_con_data[0])):
            sp_set = set()
            if Ux_con_data[i][j] == '*':
                U_Ux_sp_matrix[i].append(Ux_list)
                continue
            if j == 0 or j == 3:
                for k in range(len(U_con_data + Ux_con_data)):
                    if (U_con_data + Ux_con_data)[k][j] == '*' or abs(float(Ux_con_data[i][j]) - float((U_con_data + Ux_con_data)[k][j])) <= 0.2:
                        sp_set.add(k)
                U_Ux_sp_matrix[i].append(sp_set.copy())
            if j == 1 or j == 2:
                for k in range(len(U_con_data + Ux_con_data)):
                    if Ux_con_data[i][j] == (U_con_data + Ux_con_data)[k][j] or (U_con_data + Ux_con_data)[k][j] == '*':
                        sp_set.add(k)
                U_Ux_sp_matrix[i].append(sp_set.copy())
    U_Ux_sp_matrix = copy.deepcopy(U_sp_matrix) + U_Ux_sp_matrix
    for i in range(len(U_con_data), len(U_con_data + Ux_con_data)):
        for k in range(len(U_Ux_sp_matrix[i])):
            for j in U_Ux_sp_matrix[i][k]:
                U_Ux_sp_matrix[j][k].add(i)
    return U_Ux_sp_matrix

def get_changelist(U_Ux_sp_matrix,red_list,U_con_data): # 获得改变的相容类的下标
    U_Ux_sp_list = div_base_matric(U_Ux_sp_matrix,red_list,[])
    change_list = []
    for i in range(len(U_con_data)):
        for j in U_Ux_sp_list[i]:
            if j >= len(U_con_data):
                change_list.append(i)
                change_list.append(j)
    return set(change_list)

def merge_divlist(U_data,Ux_data,U_divlist,Ux_divlist):#      U/C + Ux/C
    U_Ux_change_divlist = []
    for i in range(len(Ux_divlist)-1,-1,-1):  #逆序循环
        for j in range(len(U_divlist)-1,-1,-1):
            if (U_data[U_divlist[j][0]] == Ux_data[(Ux_divlist[i][0]) - len(U_data)]).all():
                U_Ux_change_divlist.append(U_divlist[j] + Ux_divlist[i])
                del U_divlist[j]
                del Ux_divlist[i]
                break
    return U_Ux_change_divlist,U_divlist,Ux_divlist

def div_base_matric(Sp_matrix,con_list):
    sp_list = []
    for j in range(len(Sp_matrix)):
        sp = set(k for k in range(len(Sp_matrix)))
        for i in con_list:
            sp = sp & Sp_matrix[j][i]
        sp_list.append(list(sp.copy()))
    return sp_list

def NE_entropy(U_sp_matrix,con_list,dec_divlist):
    con_divlist = div_base_matric(U_sp_matrix,con_list)
    U_len = len(sum(dec_divlist, []))
    entropy = 0
    for j in con_divlist:
        s = list()
        for k in dec_divlist:
            intersect_set = len(set(j) & set(k))
            if intersect_set != 0:
                entropy -= (intersect_set/U_len)*math.log(intersect_set/len(j))
    return entropy

def U_Ux_add_NE_entropy(U_sp_matrix,U_Ux_sp_matrix,con_list,U_dec_divlist,U_Ux_dec_divlist):
    U_len = len(U_sp_matrix)
    U_Ux_con_divlist = div_base_matric(U_Ux_sp_matrix, con_list)
    mid = 0
    for j in range(len(U_dec_divlist)):
        if U_Ux_dec_divlist[j].__contains__(U_len):
            for i in (set(U_Ux_con_divlist[U_len]) - {U_len}):
                intersect_len = len(set(U_Ux_con_divlist[i]) & set(U_Ux_dec_divlist[j]))
                if intersect_len != 0:
                    mid += math.log(intersect_len / len(U_Ux_con_divlist[i]))
            break
    latter = 0
    for i in U_dec_divlist:
        intersect_len = len(set(i) & set(U_Ux_con_divlist[U_len]))
        if intersect_len != 0:
            latter += intersect_len * math.log(intersect_len / len(U_Ux_con_divlist[U_len]))
    return (U_len * NE_entropy(U_sp_matrix,con_list,U_dec_divlist) - mid - latter) / (U_len + 1)

def U_Ux_del_NE_entropy(U_sp_matrix,con_list,U_dec_divlist,del_list):
    U_len = len(U_sp_matrix)
    U_con_divlist = div_base_matric(U_sp_matrix,con_list)
    latter = 0
    for i in U_dec_divlist:
        intersect_len = len(set(U_con_divlist[del_list[0]]) & set(i))
        if intersect_len != 0:
            latter += intersect_len * math.log(intersect_len / len(U_con_divlist[del_list[0]]))
    return (U_len * NE_entropy(U_sp_matrix,con_list,U_dec_divlist) - latter) / (U_len - 1)

def red(U_sp_matrix,con_list,U_con_data,Ux_con_data,U_dec_divlist,U_Ux_dec_divlist,core_list,del_list):
    red_list = core_list.copy()
    if len(del_list) != 0:
        i = len(red_list) - 1
        while i >= 0:
            if U_Ux_del_NE_entropy(U_sp_matrix,set(red_list) - {red_list[i]},U_dec_divlist,del_list) - U_Ux_del_NE_entropy(U_sp_matrix,con_list,U_dec_divlist,del_list) == 0:
                del red_list[i]
                i = 0
                continue
            i = i - 1
    if len(Ux_con_data) != 0:
        U_Ux_sp_matrix = get_new_matrix(U_con_data, Ux_con_data, U_sp_matrix)
        U_Ux_con_divlist = div_base_matric(U_Ux_sp_matrix, con_list)
        U_Ux_red_divlist = div_base_matric(U_Ux_sp_matrix, red_list)
        U_len = len(U_sp_matrix)
        if U_Ux_con_divlist[U_len] == U_Ux_red_divlist[U_len]:
            print(red_list,"相容关系相等")
            return
        attr_list = list(set(con_list) - set(red_list))
        dict = {}
        red_entropy = U_Ux_add_NE_entropy(U_sp_matrix, U_Ux_sp_matrix, red_list, U_dec_divlist, U_Ux_dec_divlist)
        for i in attr_list:
            dict[i] = red_entropy - U_Ux_add_NE_entropy(U_sp_matrix, U_Ux_sp_matrix, red_list + [i], U_dec_divlist, U_Ux_dec_divlist)
        dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
        con_entropy = U_Ux_add_NE_entropy(U_sp_matrix, U_Ux_sp_matrix, con_list, U_dec_divlist, U_Ux_dec_divlist)
        while con_entropy != red_entropy:
            red_list = red_list + [attr_list[dict[0][0]]]
            del dict[0]
            red_entropy = U_Ux_add_NE_entropy(U_sp_matrix, U_Ux_sp_matrix, red_list, U_dec_divlist, U_Ux_dec_divlist)
        i = len(red_list) - 1
        while i >= 0:
            if U_Ux_add_NE_entropy(U_sp_matrix, U_Ux_sp_matrix, set(red_list) - {red_list[i]}, U_dec_divlist, U_Ux_dec_divlist) - U_Ux_add_NE_entropy(U_sp_matrix, U_Ux_sp_matrix, red_list, U_dec_divlist, U_Ux_dec_divlist) == 0:
                del red_list[i]
                i = 0
                continue
            i = i - 1
    print(red_list,"end")

if __name__ == "__main__":
    start = time.perf_counter()
    U_data = readfile("table_1.txt")
    Ux_data = readfile("add_single.txt")
    U_con_data = deal_data(U_data, len(U_data[0]) - 1, len(U_data[0]) - 1)
    U_dec_data = deal_data(U_data, 0, len(U_data[0]) - 2)
    Ux_con_data = deal_data(Ux_data, len(Ux_data[0]) - 1, len(Ux_data[0]) - 1)
    Ux_dec_data = deal_data(Ux_data, 0, len(Ux_data[0]) - 2)
    U_sp_matrix = get_matrix(U_con_data)
    con_list = [i for i in range(len(U_con_data[0]))]
    U_dec_divlist = div(U_dec_data)
    U_Ux_dec_divlist = div(U_dec_data + Ux_dec_data)
    core_list = [0, 2, 3]
    print(core_list, "core_list")
    del_list = [5]

    red(U_sp_matrix,con_list,U_con_data,Ux_con_data,U_dec_divlist,U_Ux_dec_divlist,core_list,del_list)
    # end = time.perf_counter()
    # print("time",end - start)