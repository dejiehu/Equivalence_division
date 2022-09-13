import time
from itertools import product, chain
from draw.drawing import draw_three_attribute
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

def Matrix_construct(con_data,gd_list,dec_data):  #构造基于正域的矩阵
    s = set()
    DM = [['None'] *len(con_data)  for _ in range(len(con_data))]
    for i in range(len(con_data)):
        for j in range(len(con_data)):
            s.clear()
            if  gd_list[i].__contains__(dec_data[j][0]):
                continue

            for k in range(len(con_data[0])):
                if len(eval(con_data[i][k]) & eval(con_data[j][k])) == 0:
                    s.add(k+1)
            if not not s:  #空返回False   非空True
                DM[i][j] = s.copy()
    # for i in DM:
    #     print(i)
    return DM

def Matrix_construct_partical(con_data,gd_list,con_divlist,dec_divlist,dec_data):  #构造基于正域的矩阵
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
    # print(DM_list,len(DM_list),"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
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
    return DM_list

def red_avgLength(red):
    print("约简的集合为：",red)
    num = 0
    if len(red) != 0:
        for i in red:
            num += len(i)
        print(len(red),"   ",num/len(red),"平均长度")
    print()

if __name__ == '__main__':
    list_data = readfileBylist("set_value_datasets/10%/leaf.csv")
    # list_data = readfileBylist("Parameters comparison/10%/Real estate valuation.csv")
    print(len(list_data), "对象数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    print(len(con_data[0]), "条件属性数")
    dec_divlist = div_dec(dec_data)
    for i in range(len(dec_divlist)):
        print(len(dec_divlist[i]),i)
    sort_array = []
    for i in (dec_divlist):
        sort_array += [len(i)]
    sort_array.sort()

    for i in range(len(dec_divlist)):
        if sort_array[0] == len(dec_divlist[i]):
            class_num = i
        if sort_array[1] == len(dec_divlist[i]):
            class_num_1 = i
    print(class_num, class_num_1)
    x = []
    time_list = []
    time_list_1 = []
    time_list_2 = []
    time_list_3 = []

    # con_divlist = div_byCompare(con_data)
    # gd_list = generalized_decision(con_divlist, dec_data)
    # DM = Matrix_construct(con_data, gd_list, dec_data)
    # reduct_list = Red(DM)


    for i in range(10):
        x.append(i + 1)
        temp_con_data = con_data[0:int(len(con_data) * (i + 1) / 10)]
        con_divlist = div_byCompare(temp_con_data)
        gd_list = generalized_decision(con_divlist, dec_data)

        ####
        start = time.perf_counter()
        DM_1 = Matrix_construct_partical(temp_con_data, gd_list, con_divlist, dec_divlist[24], dec_data)
        reduct_list_1 = Red(DM_1)
        time_list.append(time.perf_counter() - start)

        #单特定类
        start_1 = time.perf_counter()

        DM_1 = Matrix_construct_partical(temp_con_data,gd_list,con_divlist,dec_divlist[25],dec_data)
        reduct_list_1 = Red(DM_1)
        time_list_1.append(time.perf_counter() - start_1)

        #    单2
        start_2 = time.perf_counter()

        DM_2 = Matrix_construct_partical(temp_con_data,gd_list,con_divlist,dec_divlist[26],dec_data)
        reduct_list_2 = Red(DM_2)
        time_list_2.append(time.perf_counter() - start_2)

        #多特定类
        start_3 = time.perf_counter()
        DM_3= Matrix_construct_partical(temp_con_data,gd_list,con_divlist,dec_divlist[27],dec_data)
        reduct_list_3 = Red(DM_3)
        time_list_3.append(time.perf_counter() - start_3)
        # time_list_3.append(0)
        print("----",(i+1)*10,"%----")

    print(len(list_data), "对象数")
    print(len(con_data[0]), "条件属性数")

    print("决策类个数：", len(dec_divlist) ,sort_array)

    print("全类：")
    # red_avgLength(reduct_list)
    print("单特定类1:")
    red_avgLength(reduct_list_1)
    print("单特定类2:")
    red_avgLength(reduct_list_2)
    print("多特定类:")
    red_avgLength(reduct_list_3)
    draw_three_attribute(x,time_list,time_list_1,time_list_2,time_list_3)