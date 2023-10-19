import copy
import time
from itertools import product, chain

'''
正域保持约简
'''

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        temp_list = []
        for i in list_line:
            temp_list.append(eval(i))
        list_data.append(temp_list)
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




def div_byCompare(my_data):
    sp_list = []
    for i in range(len(my_data)):
        sp = []
        for j in range(len(my_data)):
            if insection_isEmpty(i,j,my_data):
                sp.append(j)
        sp_list.append(sp)

    return sp_list

def insection_isEmpty(i,j,my_data):
    if i == j :
        return True
    for k in range(len(my_data[0])):
        if len((my_data[i][k]) & (my_data[j][k])) == 0:
            return None
    return True

def pos(dec_divlist,con_divlist):  #子集  正域

    pos_list=[]
    for i in range(len(dec_divlist)):
         for j in range(len(con_divlist)):
            if set(con_divlist[j]).issubset(dec_divlist[i]):
                pos_list += [j]
                continue

    return pos_list

def pos_specialDec(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for j in range(len(con_divlist)):
        if set(con_divlist[j]).issubset(dec_divlist):
            pos_list += [j]
            continue
    # print(pos_list,"pos_list")
    return pos_list

def update(i,j,new_DM,s):
    if (i > j):
        new_DM[i][j] = s.copy()
    else:
        new_DM[j][i] = s.copy()
    return new_DM



def Dynamic_matrix_construct(pre_DM,pre_pos_list,new_pos_list,pre_dec_list,new_dec_list,con_data,dec_data):

    if (pre_pos_list == new_pos_list and pre_dec_list == new_dec_list):
        return pre_DM


    s_1 = time.perf_counter()

    new_DM = pre_DM
    # print(new_DM == pre_DM)
    # for i in range(len(con_data)):
    #     for j in range(i):
    #         print("ij:",i,j)
    #         if pre_DM[i][j] == 'None':
    #             continue
    #         new_DM[i][j] = pre_DM[i][j]


    # diff_dec_list = []
    # for i in pre_dec_list:
    #     if not(i in new_dec_list):
    #         diff_dec_list.append(i)
    s_2 = time.perf_counter()
    diff_dec_list = list(set(pre_dec_list) ^ set(new_dec_list))  #决策差集
    # diff_pos_list =[]
    # for i in pre_pos_list:
    #     if not(i in new_pos_list):
    #         diff_pos_list.append(i)
    diff_pos_list = list(set(pre_pos_list) ^ set(new_pos_list))  #正域差集

    # print(diff_dec_list,diff_pos_list)
    s = set()


    # print("time:s_2-s_1:", s_2 - s_1)
    if (set(new_dec_list).issubset(pre_dec_list) and pre_pos_list == new_pos_list):  #情况3
        print("情况3")
        for i in diff_dec_list:
            for j in pre_pos_list:
                s.clear()
                if not(dec_data[i] != dec_data[j]):
                    continue
                for k in range(len(con_data[0])):
                    if len((con_data[i][k]) & (con_data[j][k])) == 0:
                        s.add(k)

                new_DM = update(i, j, new_DM, s)
        return new_DM
    s_3 = time.perf_counter()
    # print("time:s_3-s_2:", s_3 - s_2)
    if (set(new_dec_list).issubset(pre_dec_list) and set(new_pos_list).issubset(pre_pos_list)):#情况4
        print("情况4")
        for i in diff_pos_list:   #删除
            for j in range(len(con_data)):
                s.clear()
                if not (j in new_pos_list):  # 删除

                    if (i > j):
                        print("删除",i,j)
                        new_DM[i][j] = 'None'
                    else:
                        print("删除",j,i)
                        new_DM[j][i] = 'None'
            for j in new_pos_list:
                s.clear()
                if(dec_data[i] != dec_data[j]):
                    for k in range(len(con_data[0])):
                        if len((con_data[i][k]) & (con_data[j][k])) == 0:
                            s.add(k)

                    new_DM = update(i, j, new_DM, s)
                    print(i,j)
        for i in diff_dec_list:
            if not(i in pre_pos_list):
                for j in new_pos_list:
                    s.clear()
                    if(dec_data[i] != dec_data[j]):
                        for k in range(len(con_data[0])):
                            if len((con_data[i][k]) & (con_data[j][k])) == 0:
                                s.add(k)
                        new_DM = update(i, j, new_DM, s)
                        print(i, j)
        s_4 = time.perf_counter()
        # print("time:s_4-s_3:",s_4-s_3)
        for s in new_DM:
            print(s)
        return new_DM


def Matrix_construct(con_data,pos_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(i):
            s.clear()
            # if not (({i}.issubset(set(pos_list)) or {j}.issubset(set(pos_list))) and dec_data[i] != dec_data[j]):
            if not ((i in pos_list or j in pos_list) and dec_data[i] != dec_data[j]):
                continue
            for k in range(len(con_data[0])):
                if len((con_data[i][k]) & (con_data[j][k])) == 0:
                    s.add(k)
            DM[i][j] = s.copy()

    # print(DM)
    # print("构造矩阵时间",time.perf_counter()-start)
    for s in DM:
        print(s)
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

def product1(fix,dis):
    result_list =[]
    for i in dis:
        for j in fix:
            temp_j=j.copy()
            temp_j.add(i)
            result_list.append(temp_j)
    return result_list

def Red(DM):#逻辑运算
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    # print("未吸收",len(DM_list), DM_list)
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    # print("多余集合被吸收",len(DM_list),DM_list)
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    loop_val = [{5},{1, 3}, {1, 4},{2, 4}]
    print(loop_val)
    DM_list = []
    if len(loop_val) > 1:  ###############################      修改过
        for i in loop_val[0]:
            DM_list.append({i})
        for i in range(1, len(loop_val)):
            DM_list = product1(DM_list, loop_val[i])
            DM_list = logic_operation(DM_list)
    elif len(loop_val) == 0:
        DM_list = loop_val.copy()
    elif len(loop_val[0]) == 1:
        DM_list = loop_val.copy()
    elif len(loop_val[0]) > 1:
        for i in loop_val[0]:
            DM_list.append({i})
    print(DM_list)
    return DM_list

def red_avgLength(red):
    print("约简的集合为：",red)
    num = 0
    if len(red) != 0:
        for i in red:
            num += len(i)
        print(len(red),"   ",num/len(red),"平均长度")
    print()
    print()

if __name__ == '__main__':

    list_data = readfileBylist("ppt_2.csv")
    # list_data = readfileBylist("Parameters comparison/10%/Real estate valuation.csv")
    print(len(list_data), "对象数2")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 2)], list_data))
    print(len(con_data[0]), "条件属性数2")

    dec_data_2 = list(map(lambda x: x[(len(list_data[0]) - 2):(len(list_data[0]) - 1)], list_data))
    dec_data_3 = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))

    dec_divlist_2 = div_dec(dec_data_2)
    dec_divlist_3 = div_dec(dec_data_3)

    con_divlist = div_byCompare(con_data)

    print(con_data)
    print(dec_data_2)
    print(dec_data_3)
    print("dec_divlist_2",dec_divlist_2)
    # print("dec_divlist_3", dec_divlist_3)
    print("con_divlist",con_divlist)



    pos_list_2 = pos_specialDec(dec_divlist_2[0], con_divlist)

    print("pos_list_2",pos_list_2)
    DM_1 = Matrix_construct(con_data, pos_list_2, dec_data_2)
    Red(DM_1)
    #
    #
    # pos_list_3 = pos_specialDec(dec_divlist_3[3], con_divlist)
    # print("pos_list_3",pos_list_3)
    # # DM_2 = Matrix_construct(con_data, pos_list_3, dec_data_3)
    # new_DM = Dynamic_matrix_construct(DM_1, pos_list_2, pos_list_3, dec_divlist_2[1], dec_divlist_3[3],con_data,dec_data_3)
    # Red(new_DM)

    # for s in range(len(DM_2)):
    #     if (DM_2[s] != new_DM[s]):
    #         print("竟然有不相等的")




