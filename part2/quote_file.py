from itertools import chain


def deal_data(my_data,m):#处理数据表
    del_data = [my_data[i][:] for i in range(len(my_data))]
    for d in range(len(del_data)):
        del del_data[d][m]
    return del_data

def Max_min(con_data,U_list):  #找出属性最大最小值
    Mm_list = []
    # print("1")
    # print(len(con_data[0]))
    for i in range(len(con_data[0])):
        min = 10000
        Max = 0
        # print("4")
        for j in U_list:
            # print("2")
            if con_data[j][i] > Max:
                Max = con_data[j][i]
                continue
            if con_data[j][i] < min:
                # print("3")
                min = con_data[j][i]
        Mm_list.append([Max,min])
    return Mm_list

def div(my_data):    #等价类的划分
    U_linkList =  [i for i in range(len(my_data))]
    Mm_list = Max_min(my_data,U_linkList)
    for i in range(len(Mm_list)):
        queue_linkList = [[]]*(Mm_list[i][0] - Mm_list[i][1] + 1)
        for j in U_linkList:
            queue_linkList[my_data[j][i] - Mm_list[i][1]] = queue_linkList[my_data[j][i] - Mm_list[i][1]] + [j]
        U_linkList.clear()
        U_linkList = list(chain.from_iterable(queue_linkList))
    div_list = []
    temp_list = [U_linkList[0]]
    for i in range(1,len(U_linkList)):
        if((my_data[U_linkList[i]] == my_data[U_linkList[i-1]])):
            temp_list.append(U_linkList[i])
            continue
        div_list.append(temp_list)
        temp_list = [U_linkList[i]]
    div_list.append(temp_list)
    return div_list

def getCore_data(core_list,con_data):    #从所有数据中取出核属性数据
    core_data = []
    for data_row in con_data:
        core_data.append([data_row[i] for i in core_list])
    return core_data

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

def data_add(src_data,tag_data,col):  #添加一列
    tag_copy = [tag_data[i][:] for i in range(len(tag_data))]
    for i in range(len(tag_copy)):
        tag_copy[i] += [src_data[i][col]]
    return tag_copy