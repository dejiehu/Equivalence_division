import time
from itertools import product
'''
正域保持约简
'''
from part2.quote_file import div

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data


def pos(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
                continue
    # print(pos_list,"pos_list")
    return pos_list

def Matrix_construct(con_data,pos_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            if not({i}.issubset(set(pos_list)) or {j}.issubset(set(pos_list))):
                continue
            if dec_data[i][0] == dec_data[j][0]:
                continue
            for k in range(len(con_data[0])):
                if(con_data[i][k] != con_data[j][k]):
                    s.add(k)
            DM[i][j] = s.copy()
    return DM
'''
耗时间
'''
def logic_operation(diffItem_list):#析取，吸收
    DM_list = sorted(diffItem_list, key=lambda i: len(i), reverse=False)
    # print(DM_list,"paixushuchu ")
    m = len(DM_list) - 1# 吸收多余的集合
    while m > 0: #m从后往前
        n = 0  #从前往后
        while n < m:
            if set(DM_list[n]).issubset(DM_list[m]):
                del DM_list[m]
                m = len(DM_list)
                break
            n += 1
        m -= 1
    return DM_list

def Red(DM):#逻辑运算
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,len(DM_list),"多余集合被吸收")
    loop_val = []     #将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    # print(loop_val)
    DM_list = []
    for i in product(*loop_val):
        DM_list.append(set(i))
    print("分配节结束")
    # print(DM_list.__len__(),DM_list)
    DM_list = logic_operation(DM_list)
    print("约简的集合为：",len(DM_list), DM_list)

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("../complete_dataSet_classication/Teaching Assistant Evaluation.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    pos_list = pos(dec_divlist,con_divlist)
    DM = Matrix_construct(con_data,pos_list,dec_data)
    Red(DM)
    # loop_val = [{0}, {9, 5}, {1, 3}, {1, 6}, {8, 4}, {8, 1}, {1, 4, 7}, {9, 3, 7}, {9, 4, 6}, {9, 4, 7}, {1, 2, 4}, {2, 4, 7}, {9, 2, 4}, {9, 3, 4}, {3, 4, 5}, {2, 3, 4}, {2, 5, 6}, {2, 3, 5}, {8, 9, 3}, {2, 4, 6}, {8, 6, 7}, {9, 2, 6, 7}, {4, 5, 6, 7}, {9, 2, 3, 6}]
    # DM_list = []
    # for i in product(*loop_val):
    #     DM_list.append(set(i))
    # print(len(DM_list))

    end = time.perf_counter()
    print(end - start, "time")
