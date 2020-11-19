import numpy

def readfile():
    my_data = numpy.loadtxt('data.txt')
    print(my_data)
    return my_data


def con_div(my_data):
    con_divlist = []  # 条件
    jump = 1
    list2 = []  # 条件
    for i in range(len(my_data)): #8行
        list2.clear()
        for l in range(len(con_divlist)):
            if (con_divlist[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list2.append(i)
        for k in range(i+1,len(my_data)):
            if((my_data[i][0] == my_data[k][0]) & (my_data[i][1] == my_data[k][1]) &(my_data[i][2] == my_data[k][2]) &(my_data[i][3] == my_data[k][3])):
                list2.append(k)
        con_divlist.append(list2.copy())
        print(con_divlist,"con_divlist")
    return con_divlist


def dec_div(my_data):
    dec_divlist = []  #决策
    jump = 1
    list1 = []#决策

    for i in range(len(my_data)): #8行
        list1.clear()
        for l in range(len(dec_divlist)):
            if (dec_divlist[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list1.append(i)
        for j in range(i+1,len(my_data)):
            if((my_data[i][my_data.shape[1]-1] == my_data[j][my_data.shape[1]-1])):
                list1.append(j)
                print(j)
        dec_divlist.append(list1.copy())
        print(dec_divlist,"dec_divlist")
    return dec_divlist


def pos(dec_divlist,con_divlist):
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    print(pos_list)


my_data = readfile()
dec_divlist = dec_div(my_data)
con_divlist = con_div(my_data)
pos(dec_divlist,con_divlist)