import numpy

def readfile():
    my_data = numpy.loadtxt('data.txt')
    print(my_data)
    return my_data

def div(my_data,m,n): #1.数据表，2、3.删除元素下表
    divlist =[]#返回的划分集合
    list = []
    jump = 1
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    for i in range(len(my_data)):  # 8行
        list.clear()
        for l in range(len(divlist)):
            if (divlist[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list.append(i)
        for j in range(i + 1, len(my_data)):
            if ((my_data[i] == my_data[j]).all()):
                list.append(j)
        divlist.append(list.copy())
    return divlist

def pos(dec_divlist,con_divlist):  #子集
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    print(pos_list)


my_data = readfile()
con_divlist = div(my_data,3,4)
print(con_divlist,"con_divlist")
dec_divlist = div(my_data,0,2)
print(dec_divlist,"dec_divlist")
pos(dec_divlist,con_divlist)
















