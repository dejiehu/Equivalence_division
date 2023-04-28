import time
from itertools import product, chain
from draw.drawing import draw_four_universe_two
'''
不完备正域保持约简
'''

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
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
        if len(eval(my_data[i][k]) & eval(my_data[j][k])) == 0:
            return None
    return True

def generalized_decision(con_divlist,dec_data):
    gd_list=[]
    for i in con_divlist:
        gd_set = set()
        for j in i:
            gd_set.add((dec_data[j][0]))
        gd_list.append(list(gd_set))
    # print(gd_list)
    return gd_list

def Matrix_construct(con_data,gd_list,dec_data):  #构造基于广义决策的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(len(con_data)):
            s.clear()
            if  gd_list[i].__contains__(dec_data[j][0]):
                continue
            # if gd_list[i] == gd_list[j] :
            #     continue
            for k in range(len(con_data[0])):
                if len(eval(con_data[i][k]) & eval(con_data[j][k])) == 0:
                    s.add(k+1)
            if not not s:  #空返回False   非空True
                DM[i][j] = s.copy()
    # for i in DM:
    #     print(i)
    return DM

def Matrix_construct_partical(con_data,gd_list,con_divlist,dec_divlist,dec_data):  #构造基于广义决策的矩阵局部
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(len(con_data)):
            s.clear()
            if gd_list[i].__contains__(dec_data[j][0]):
                continue
            if set(dec_divlist).isdisjoint(con_divlist[i]):  #判断两集合是否包含相同元素
                continue

            for k in range(len(con_data[0])):
                if len(eval(con_data[i][k]) & eval(con_data[j][k])) == 0:
                    s.add(k+1)
            if not not s:  # 空返回False   非空True
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

def product1(fix,dis):
    result_list =[]
    for i in dis:
        for j in fix:
            temp_j=j.copy()
            temp_j.add(i)
            result_list.append(temp_j)
    return result_list

def shortest_Red(DM,con_data):#逻辑运算d
    DM_list = []
    for i in range(len(DM)):   #矩阵差别项放到集合DM_list中
        for j in range(len(DM)):
            if DM[i][j] == 'None':#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    # print(DM_list,len(DM_list),"多余集合被吸收")
    # DM_list = [{1,3},{1,2,4},{1,4,8},{1,2,9},{3,7,12},{3,6,13},{2,5},{4,10},{11}]  #test.txt
    # DM_list = [{2,3,4,5}, {4,5,7,8,} ,{1,4,7,9}, {1,2,3,8}, {2,3,7,8}, {1,7,8}, {1,4,5}, {3,4,5,7}, {1,3,7}, {2,3,5,7}, {1,4,5,8}, {1,2,3,9}, {3,7,8,9}, {1,2,5,8,9}, {1,3,4,8,9},{6},{2,5,7,8,9},{1,2,4,7},{2,3,4,8},{1,3,5}]
    # DM_list = [{5},{1,4}] set_speed.txt
    Reduct = []
    MinReduct = [i for i in range(len(con_data[0]))]
    CAMARDF(DM_list,Reduct,MinReduct,con_data)

    return MinReduct

def sort_dict(DF): #根据出现次数排序
    sig_dict = dict()
    for i in DF:
        if i.__len__()==0:
            continue
        for j in i:
            if j in sig_dict:
                sig_dict[j] = sig_dict[j] + 1
            else:
                sig_dict[j] = 1
    sig_dict["x"] = 0
    sig_dict = sorted(sig_dict.items(),key=lambda x: x[1], reverse=True)   #根据字典value排序
    return sig_dict

def delete_attribute(DF,index):   #根据索引删除属性，索引=属性
    for i in range(len(DF)):
        DF[i].discard(index)

def delete_disjunction(DF,index):   #根据索引删除属性所在的差别项，索引=属性
    temp_DF = []
    for i in range(len(DF)):
        if(index not in DF[i]):
            temp_DF.append(DF[i])
    return temp_DF


def CAMARDF(DF,Reduct,MinReduct,con_data):
    if (DF.__len__() == 0):
        return
    sig_dict = sort_dict(DF)
    i = 0
    while(True):
        if(Reduct.__len__() + 1 == MinReduct.__len__()):
            return
        if(i > 0):
            delete_attribute(DF, sig_dict[i-1][0])
            for j in DF:
                if(j.__len__() == 0):
                    return
        Reduct.append(sig_dict[i][0])
        temp_DF = delete_disjunction(DF, sig_dict[i][0])
        if (temp_DF.__len__() == 0):
            if(MinReduct.__len__() > Reduct.__len__()):
                MinReduct.clear()
                MinReduct += Reduct
                # print("get new result,change the minReduct:",MinReduct)
        else:
            CAMARDF(temp_DF,Reduct,MinReduct,con_data)
        Reduct.remove(sig_dict[i][0])
        i += 1
        if(sig_dict[i][1] <= 1 or i >= len(con_data[0])):
            break


if __name__ == '__main__':
    list_data = readfileBylist("set_value_datasets/10%/Speaker Accent Recognition.csv")
    print(len(list_data), "对象数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    print(len(con_data[0]), "条件属性数")
    dec_divlist = div_dec(dec_data)

    # for i in range(len(dec_divlist)):
        # print(len(dec_divlist[i]),i,dec_data[dec_divlist[i][0]][0])
    sort_array = []
    for i in (dec_divlist):
        sort_array += [len(i)]
    sort_array.sort()
    #
    for i in range(len(dec_divlist)):
        if sort_array[0] == len(dec_divlist[i]):
            class_num = 0
        if sort_array[1] == len(dec_divlist[i]):
            class_num_1 = 3
    print(dec_data[dec_divlist[class_num][0]][0],dec_data[dec_divlist[class_num_1][0]][0])
    x = []
    time_list = []
    time_list_1 = []

    for i in range(10):
        x.append(i + 1)
        temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]

        con_divlist = div_byCompare(temp_con_data)
        gd_list = generalized_decision(con_divlist, dec_data)
        start = time.perf_counter()
        gd_list = generalized_decision(con_divlist, dec_data)
        # print(gd_list)
        #全类

        DM = Matrix_construct(temp_con_data, gd_list, dec_data)
        MinReduct = shortest_Red(DM,temp_con_data)
        time_list.append(time.perf_counter() - start)
    #     # #单特定类
        start_1 = time.perf_counter()
        DM_1 = Matrix_construct_partical(temp_con_data,gd_list,con_divlist,dec_divlist[class_num],dec_data)
        MinReduct_1 = shortest_Red(DM_1,temp_con_data)
        time_list_1.append(time.perf_counter() - start_1)


        #    单2
        # start_2 = time.perf_counter()
        # DM_2 = Matrix_construct_partical(temp_con_data,gd_list,con_divlist,dec_divlist[class_num_1],dec_data)
        # MinReduct_2 = Red(DM_2)
        # time_list_2.append(time.perf_counter() - start_2)
        # time_list_2.append(0)


        print("----",(i+1)*10,"%----")

    print(len(list_data), "对象数")
    print(len(con_data[0]), "条件属性数")

    print("决策类个数：", len(dec_divlist) ,sort_array)

    print("全类：")
    print(set(MinReduct),len(MinReduct))
    print("单特定类1:")
    print(set(MinReduct_1), len(MinReduct_1))
    # print("单特定类2:")
    # red_avgLength(reduct_list_2)

    print(time_list)
    print(time_list_1)

    draw_four_universe_two(x,time_list,time_list_1)