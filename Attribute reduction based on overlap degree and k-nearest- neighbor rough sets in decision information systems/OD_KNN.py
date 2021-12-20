import time
# from part2.quote_file import div,deal_data,getCore_data,del_dup,data_add,deal_sample

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(' ')
        s = [float(j) for j in list_line]
        list_data.append(s)
    return list_data

def div(my_data):  #划分等价类
    div_list = []
    jump = 1
    list1= []
    for i in range(len(my_data)):
        list1.clear()
        for l in range(len(div_list)):
            if (div_list[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list1.append(i)
        for j in range(i+1,len(my_data)):
            if((my_data[i] == my_data[j])):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

def get_max_min(D,attribution):
    max = attribution[D[0]]
    min = attribution[D[0]]
    for i in D:
        if max < attribution[D[i]]:
            max = attribution[D[i]]
        if min > attribution[D[i]]:
            min = attribution[D[i]]
    return max,min

def get_colum(colum,data):
    colum_list =[]
    for i in data:
        colum_list += [i[colum]]
    return colum_list

def CD_attr(Di,Dj,attribution):
    max_i, min_i = get_max_min(Di,attribution)
    max_j, min_j = get_max_min(Dj,attribution)
    if min_i > max_j or min_j > max_i:
        CD = (min(max_i, max_j) - max(min_i, min_j) + 0.1) / 0.1
    else:
        CD = (min(max_i, max_j) - max(min_i, min_j)) / (min(max_i, max_j) - max(min_i, min_j))
    return CD

def get_attribution(D,attribution):
    D_list = []
    for i in D:
        D_list += attribution[i]
    return D_list

def DIS_attr(Di,Dj,attribution):
    Di_list = get_attribution(Di, attribution)
    Dj_list = get_attribution(Dj, attribution)
    Di_avg = sum(Di_list) / len(Di)
    Dj_avg = sum(Dj_list) / len(Dj)
    DIS = abs(Di_avg - Dj_avg) / (max(Di_list + Dj_list) - min(Di_list + Dj_list))
    return DIS


if __name__ == '__main__':
    start = time.perf_counter()
    list_data = readfileBylist("data.txt")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    dec_divlist = div(dec_data)
    for k in range(len(con_data[0])):
        CD = 0
        DIS = 0
        attr_data = get_colum(k, con_data)
        for i in range(len(dec_divlist)-1,-1,-1):
            for j in range(i):
                CD += CD_attr(dec_divlist[i],dec_divlist[j],attr_data)
                DIS += DIS_attr(dec_divlist[i],dec_divlist[j],attr_data)
