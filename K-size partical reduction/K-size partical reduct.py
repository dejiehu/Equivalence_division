import math
import random
import time
from part2.quote_file import div,deal_data,getCore_data,del_dup,data_add,deal_sample

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    temp_con_divlist = [con_divlist[i][:] for i in range(len(con_divlist))]
    for i in dec_divlist:
         for j in range(len(temp_con_divlist)-1,-1,-1):
            if set(temp_con_divlist[j]).issubset(i):
                pos_list += temp_con_divlist[j]
                del temp_con_divlist[j]
    return  pos_list

def InitialSolution(con_data,dec_data,pos_list):
    red_list = []
    red_data = [[]]*len(con_data)
    redp_list = []
    attr_list = [i for i in range(len(con_data[0]))]
    attr_data = [con_data[i][:] for i in range(len(con_data))]
    while set(pos_list) != set(redp_list):
        iop_num = 1000000
        U_list = list(set(pos_list) - set(redp_list))
        temp_dec_data = deal_sample(U_list,dec_data)
        temp_attr_data = deal_sample(U_list, attr_data)
        U_list = [i for i in range(len(temp_dec_data))]
        for i in range(len(attr_list)):
            iop_list = set(U_list) - set(pos(div(temp_dec_data),div(list(map(lambda x: x[i:i+1], temp_attr_data)))))
            if len(iop_list) < iop_num:
                iop_num = len(iop_list)
                min_attr = i
        red_list = red_list + [attr_list[min_attr]]
        del attr_list[min_attr]
        red_data = data_add(attr_data,red_data,min_attr)
        attr_data = deal_data(attr_data,min_attr)
        redp_list = pos(div(dec_data),div(red_data))
    print("red_list",red_list)
    return red_data,red_list

def GenerateSolution(con_data,dec_data,red_data,red_list,pos_list,weight_list):
    redp_list = pos(div(dec_data), div(red_data))
    U_list = list(set(pos_list) - set(redp_list))
    #过滤集
    add_filter = []
    attr_data,attr_list = del_dup(con_data,red_list)
    temp_dec_data = deal_sample(U_list, dec_data)
    temp_attr_data = deal_sample(U_list, attr_data)
    U_list = [i for i in range(len(temp_dec_data))]
    for i in range(len(attr_list)):
        if set(U_list) == set(pos(div(temp_dec_data),div(list(map(lambda x: x[i:i+1], temp_attr_data))))):
            add_filter += [attr_list[i]]
            # break
    if len(add_filter) == 0:
        temp_weight_list = weight_list.copy()
        for i in range(len(temp_weight_list)):
            if not U_list.__contains__(i):
                temp_weight_list[i] = -1
        x = temp_weight_list.index(max(temp_weight_list))
        dic_list = []
        for i in range(len(attr_list)):
            num = 0
            cmp_list = list(map(lambda x: x[i:i + 1], temp_attr_data))
            for i in range(len(cmp_list)):
                if i == x:
                    continue
                if cmp_list[x] != cmp_list[i] and temp_dec_data[x] != temp_dec_data[i]:
                    num += 1
            dic_list += [num]
        add_filter += [attr_list[dic_list.index(max(dic_list))]]
    #删除集
    del_filter = []
    red_data = data_add(attr_data, red_data, attr_list.index(add_filter[0]))
    for i in range(len(red_list)):
        temp_red_data = deal_data(red_data,i)
        after_pos_list = pos(div(dec_data),div(temp_red_data))
        if len(after_pos_list) > len(redp_list):
            del_filter += [red_list[i]]
    if len(del_filter) == 0:
        sig = 100000
        for i in range(len(red_list)):
            temp_red_del_data = deal_data(red_data, i)
            sig_inter = len(pos(div(dec_data), div(red_data))) - len(pos(div(dec_data), div(temp_red_del_data)))
            if sig >= sig_inter:
                sig = sig_inter
                index_value = i
        del_filter += [red_list[index_value]]
    red_list += [add_filter[0]]
    red_data = deal_data(red_data,red_list.index(del_filter[0]))
    del red_list[red_list.index(del_filter[0])]
    # print(red_list,"new_red_list")
    return red_data,red_list

def WeightingStrategy(red_list,pos_list,weight_list,arg1,arg2):
    for i in range(len(pos_list)):
        if not red_list.__contains__(pos_list[i]):
            weight_list[i] += 1
    if sum(weight_list)/len(weight_list) > arg1:
        for i in range(len(pos_list)):
            weight_list[i] *= arg2
    return weight_list

def LSAR(con_data,dec_data):
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    pos_list = pos(dec_divlist, con_divlist)
    red_data,red_list = InitialSolution(con_data,dec_data,pos_list)
    weight_list = []
    for i in range(len(pos_list)):
        weight_list += [0]
    t = 0
    T = 50
    while T > t:
        if set(pos_list) == set(pos(div(dec_data),div(red_data))):
            temp_red_list = red_list.copy()
            a = random.randint(0, len(temp_red_list) - 1)
            del temp_red_list[a]
            temp_red_data = deal_data(red_data, a)
        if set(pos_list) == set(pos(div(dec_data),div(temp_red_data))):
            red_list = temp_red_list.copy()
            red_data = [temp_red_data[i][:] for i in range(len(temp_red_data))]
        else:
            temp_red_data,temp_red_list = GenerateSolution(con_data, dec_data, temp_red_data,temp_red_list,pos_list,weight_list)
            if set(pos_list) == set(pos(div(dec_data),div(temp_red_data))):
                red_list = temp_red_list.copy()
                red_data = [temp_red_data[i][:] for i in range(len(temp_red_data))]
                for i in range(len(pos_list)):
                    weight_list[i] = 0
            else:
                weight_list = WeightingStrategy(red_list, pos_list, weight_list, 2, 0.1)
        t += 1
    print(red_list, len(red_list))

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("../complete_dataSet_classication/german_o.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    LSAR(con_data,dec_data)
    end =  time.perf_counter()
    print("time",end - start)
