import time
from itertools import chain

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        list_data.append(list_line)
    return list_data

def deal_data(my_data,m):#处理数据表
    del_data = [my_data[i][:] for i in range(len(my_data))]
    for d in range(len(del_data)):
        del del_data[d][m]
    return del_data

def div(my_data): #1.数据表，2、3.删除元素下表   求划分集合
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

def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核
    core_list = []
    for i in range(len(con_data[0])-1,-1,-1):
        temp_con_data = deal_data(con_data,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        if dep_num != dependency(pos_list,con_data):
            print("第",i+1,"个属性为核属性")
            core_list.append(i)
    print(core_list,"core_list")
    return core_list

def dependency(pos_list,my_data): #依赖度
     dep_num =  (len(pos_list) / len(my_data))
     # print("依赖度:",dep_num)
     return dep_num

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:      #    for i in itertools.product(dec_divlist,con_divlist):--产生笛卡尔积
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
                continue
    # print(pos_list,"pos_list")
    return  pos_list

def getCore_data(core_list,con_data):    #从所有数据中取出核属性数据
    core_data = []
    for data_row in con_data:
        core_data.append([data_row[i] for i in core_list])
    return core_data

def data_add(src_data,tag_data,col):  #添加一列
    tag_copy = [tag_data[i][:] for i in range(len(tag_data))]
    for i in range(len(tag_copy)):
        tag_copy[i] += src_data[i][col]
    return tag_copy

def del_dup(con_data,core_list):  #找出未被添加的属性
    attr_list = [i for i in range(len(con_data[0]))]
    att_data = [con_data[i][:] for i in range(len(con_data))]
    j = len(con_data) - 1
    while j >= 0:
        if core_list.__contains__(j):
            att_data = deal_data(att_data,j)
            del attr_list[j]
        j -= 1
    return att_data,attr_list

def Red(con_data,dec_divlist,core_list,dep_num):  # 求约简
    core_data = getCore_data(core_list,con_data)
    core_dep = dependency(pos(dec_divlist,div(core_data)),con_data)
    Red_data = [core_data[i][:] for i in range(len(core_data))]
    core_list = sorted(core_list,reverse=True)
    red_list = core_list.copy()
    att_data,attr_list = del_dup(con_data,core_list)
    Red_dep = core_dep
    dict = {}#字典存放添加的依赖度
    num = 0
    print(Red_dep, dep_num)
    while Red_dep != dep_num:
        # print(Red_dep, dep_num)
        # print("第",num,"次循环了")
        num += 1
        dict.clear()
        con_key = -1#字典key
        con_value = 0#字典value
        for k in range(len(att_data[0])):
            temp_Red_data = data_add(att_data,Red_data,k)
            Red_divlist = div(temp_Red_data)
            dict[k] = dependency(pos(dec_divlist,Red_divlist),con_data) - Red_dep
        # print(dict)
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        # print(dict)
        Red_data = data_add(att_data,Red_data,con_key)
        red_list.append(attr_list[con_key])
        del attr_list[con_key]
        att_data = deal_data(att_data,con_key)
        Red_dep = dependency(pos(dec_divlist,div(Red_data)), con_data)#添加条件属性后的依赖度
        # print(Red_dep)
    print(red_list,"red_list")
    return Red_data,red_list

def De_redundancy(Red_data,dec_divlist,dep_num,red_list):# 去冗余
    i = 0
    while i < len(Red_data[0]):
        temp_Red_data = deal_data(Red_data,i)
        dep = dependency(pos(dec_divlist, div(temp_Red_data)), Red_data)
        if dep_num == dep:
            Red_data = deal_data(Red_data,i)
            del red_list[i]
            i = 0
            continue
        i += 1
    print(red_list,"去冗余red_list")

if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("data.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0])-1)],list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0])-1):],list_data))
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    dep_num = dependency(pos(dec_divlist,con_divlist),list_data)
    core_list = core(con_data, dec_divlist, dep_num)
    Red_data,red_list = Red(con_data, dec_divlist, core_list, dep_num)
    De_redundancy(Red_data, dec_divlist, dep_num, red_list)
    end = time.perf_counter()
    print("time:",end - start)