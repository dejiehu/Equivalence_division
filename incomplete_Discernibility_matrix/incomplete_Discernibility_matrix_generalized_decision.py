import time
from itertools import product, chain

'''
不完备正域保持约简
'''

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(',')
        list_data.append(list_line)
    return list_data

def div_dec(my_data): #
    div_list =[]#返回的划分集合
    list1 = []
    for i in range(len(my_data)):  #
        list1.clear()
        if list(chain.from_iterable(div_list)).__contains__(i):  # 展开
            continue
        list1.append(i)
        for j in range(i + 1, len(my_data)):
            if ((my_data[i] == my_data[j])):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

def get_matrix(my_data): #多个对象的相容类等于单个对象的交集
    Sp_matrix = [[] for i in range(len(my_data))]
    for i in range(len(my_data)):
        for j in range(len(my_data[0])):
            sp_set = set()
            for k in range(len(my_data)):
                if my_data[i][j] ==my_data[k][j] or my_data[i][j] == '?' or my_data[k][j] == '?':
                    sp_set.add(k)
            Sp_matrix[i].append(sp_set.copy())
    return Sp_matrix

def div_base_matric(Sp_matrix):  #相容类下用交集求划分
    sp_list = []
    for j in range(len(Sp_matrix)):
        sp = set(k for k in range(len(Sp_matrix)))
        for i in range(len(Sp_matrix[0])):
            sp = sp & Sp_matrix[j][i]
        sp_list.append(list(sp.copy()))
    return sp_list

def generalized_decision(con_divlist,dec_data):
    gd_list=[]
    for i in con_divlist:
        gd_set = set()
        for j in i:
            gd_set.add(dec_data[j][0])
        gd_list.append(list(gd_set))
    # print(gd_list)
    return gd_list

def Matrix_construct(con_data,gd_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            if  gd_list[i].__contains__(dec_data[j][0]):
                continue
            for k in range(len(con_data[0])):
                if (con_data[i][k] != con_data[j][k] and con_data[i][k] != '?' and con_data[j][k] != '?'):
                    s.add(k)
            if len(s)!=0:
                DM[i][j] = s.copy()
    # for i in DM:
    #     print(i)
    return DM
'''
耗时间
'''
def logic_operation(diffItem_list):#析取，吸收
    DM_list = sorted(diffItem_list, key=lambda i: len(i), reverse=False)
    m = len(DM_list) - 1# 吸收多余的集合
    while m > 0: #m从后往前
        n = 0  #从前往后
        while n < m:
            if set(DM_list[n]).issubset(DM_list[m]):
                del DM_list[m]
                break
            n += 1
        m -= 1
    return DM_list

def Red(DM):#逻辑运算d
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(len(DM)):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,len(DM_list),"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    DM_list = []
    for i in product(*loop_val):
        DM_list.append(set(i))
    DM_list = logic_operation(DM_list)
    print("约简的集合为：",len(DM_list), DM_list,"约简个数")
    num = 0
    for i in DM_list:
        num += len(i)
    print(num/len(DM_list),"平均长度")

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("../incomplete_dataSet/lymph_incomplete.txt")
    # list_data = readfileBylist("../Qualitative_Bankruptcy.txt")
    print(len(list_data),"对象数")
    print(len(list_data[0])-1,"条件属性数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    num_list = []
    for i in dec_data:
        if num_list.__contains__(i[0]):
            continue
        num_list.append(i[0])
    print(num_list,len(num_list),"决策数")
    con_divlist = div_base_matric(get_matrix(con_data))
    dec_divlist = div_dec(dec_data)
    # print("con_divlist", con_divlist)
    # print("dec_divlist", dec_divlist)
    gd_list = generalized_decision(con_divlist,dec_data)
    DM = Matrix_construct(con_data,gd_list,dec_data)
    Red(DM)
    end = time.perf_counter()
    print(end - start, "time")
