import copy
import time
from itertools import chain


def readfile(file_name):#读文件
    con_data = []
    f = open(file_name, "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    for i in range(0, lines.__len__(), 1):  # (开始/左边界, 结束/右边界, 步长)
        list = []  ## 空列表, 将第i行数据存入list中
        for word in lines[i].split():
            word = word.strip()
            list.append(word)
        con_data.append(list)
    print(con_data)
    return con_data

def deal_data(con_data,m,n):#处理数据表
    data = [con_data[i][:] for i in range(len(con_data))]
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

def get_matrix(con_data): #
    U_list = {i for i in range(len(con_data))}
    Sp_matrix = [[] for i in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(len(con_data[0])):
            sp_set = set()
            index = 1
            for k in range(len(con_data)):
                if con_data[i][j] == '*':
                    Sp_matrix[i].append(U_list)
                    index = 0
                    break
                if con_data[i][j] == con_data[k][j] or con_data[k][j] == '*':
                    sp_set.add(k)
            if index == 1:
                Sp_matrix[i].append(sp_set.copy())
    return Sp_matrix

def div_base_matric(Sp_matrix,con_list):
    sp_list = []
    for j in range(len(Sp_matrix)):
        sp = Sp_matrix[j][con_list[0]]
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

def RED(Sp_matrix,con_list,dec_divlist):
    con_divlist = div_base_matric(Sp_matrix, con_list)
    pos_c = pos(dec_divlist,con_divlist)
    dict = {}
    for i in range(len(con_list)):
        print(con_list)
        print(set(con_list) - {con_list[i]})
        temp_divlist = div_base_matric(Sp_matrix,list(set(con_list) - {con_list[i]}))
        dict[i] = len(pos_c) - len(pos(dec_divlist,temp_divlist))
    print(dict)


if __name__ == "__main__":
    start = time.perf_counter()
    my_data = readfile("table.txt")
    con_data = deal_data(my_data, len(my_data[0]) - 1, len(my_data[0]) - 1)
    dec_data = deal_data(my_data, 0, len(my_data[0])  - 2)
    Sp_matrix = get_matrix(con_data)
    con_list = [i for i in range(len(con_data[0]))]
    dec_divlist = div(dec_data)
    RED(Sp_matrix, con_list, dec_divlist)