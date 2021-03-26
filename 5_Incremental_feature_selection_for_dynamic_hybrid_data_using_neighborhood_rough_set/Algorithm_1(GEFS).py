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

def get_matrix(con_data): #
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

def div_base_matric(Sp_matrix,con_list):
    sp_list = []
    for j in range(len(Sp_matrix)):
        sp = set(k for k in range(len(Sp_matrix)))
        for i in con_list:
            sp = sp & Sp_matrix[j][i]
        sp_list.append(list(sp.copy()))
    return sp_list

def NE_entropy(U_sp_matrix,con_list,dec_divlist):
    con_divlist = div_base_matric(U_sp_matrix, con_list)
    U_len = len(sum(dec_divlist, []))
    entropy = 0
    for j in con_divlist:
        s = list()
        for k in dec_divlist:
            intersect_set = len(set(j) & set(k))
            if intersect_set != 0:
                entropy -= (intersect_set/U_len)*math.log(intersect_set/len(j))
    return entropy

def core(U_sp_matrix,con_list,dec_divlist,ne_entropy):# 根据 属性重要度  求核
    core_list = []
    for i in con_list:
        if NE_entropy(U_sp_matrix,list(set(con_list) - {i}).copy(),dec_divlist) - ne_entropy > 0:
            core_list.append(i)
    return core_list

def red(U_sp_matrix,con_list,dec_divlist,core_list,ne_entropy):
    red_list = core_list.copy()
    attr_list = list(set(con_list) - set(red_list))
    while ne_entropy != NE_entropy(U_sp_matrix,red_list,dec_divlist):
        dict = {}
        con_key = -1  # 字典key
        con_value = -1  # 字典value
        for i in attr_list:
            dict[i] = ne_entropy - NE_entropy(U_sp_matrix,red_list + [i],dec_divlist)
        for key in dict:
            if dict[key] > con_value:
                con_value = dict[key]
                con_key = key
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
    print(red_list)
    # De_redundancy(U_sp_matrix,dec_divlist,red_list,ne_entropy)

# def De_redundancy(U_sp_matrix,dec_divlist,red_list,ne_entropy):
#     i =  len(red_list) - 1
#     while i >= 0:
#         if ne_entropy == NE_entropy(U_sp_matrix,set(red_list) - {i},dec_divlist):
#             print(i,red_list[i])
#             del red_list[i]
#             i = 0
#         i = i - 1
#     print(red_list)

if __name__ == "__main__":
    start = time.perf_counter()
    U_data = readfile("table_1.txt")
    U_con_data = deal_data(U_data, len(U_data[0]) - 1, len(U_data[0]) - 1)
    U_dec_data = deal_data(U_data, 0, len(U_data[0])  - 2)
    U_sp_matrix = get_matrix(U_con_data)
    print(U_sp_matrix,"U")
    con_list = [i for i in range(len(U_con_data[0]))]
    U_dec_divlist = div(U_dec_data)
    ne_entropy = NE_entropy(U_sp_matrix,con_list, U_dec_divlist)
    core_list = core(U_sp_matrix, con_list, U_dec_divlist,ne_entropy)
    print(core_list,"core_list")
    red(U_sp_matrix,con_list,U_dec_divlist,core_list,ne_entropy)
    # end = time.perf_counter()
    # print("time",end - start)