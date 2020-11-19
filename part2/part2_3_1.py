import numpy

def readfile():
    my_data = numpy.loadtxt('table_1.txt')
    print(my_data)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

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
            if((my_data[i] == my_data[j]).all()):
                list1.append(j)
        div_list.append(list1.copy())
    return div_list

def pos(dec_divlist,con_divlist):  #子集  正域
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    print(pos_list)
    return pos_list

def Matrix_construct(my_data,pos_list,con_divlist):  #构造基于正域的矩阵
    s = set()
    DM = numpy.zeros(shape=(len(my_data), len(my_data)), dtype = tuple)
    for i in range(len(DM)):
        DM[i] = None
    for i in range(my_data.shape[0]):
        for j in range(i):
            s.clear()
            index = 0
            for m in range(len(con_divlist)):
                if con_divlist[m].__contains__(i):
                    print(m,i)
                    if set(con_divlist[m]).issubset(set(pos_list)):
                        print(set(con_divlist[m]),set(pos_list),"子集")
                        break
                if m == len(con_divlist) - 1:
                    index = len(con_divlist) - 1
            if index == len(con_divlist) - 1:
                DM[i][j] = None
                continue
            for k in range(my_data.shape[1]):
                if(my_data[i][k] != my_data[j][k]):
                    s.add(k)
            DM[i][j] = s.copy()
    print(DM)
    return DM

if __name__ == '__main__':
    my_data = readfile()
    con_data = deal_data(my_data,2,2)
    dec_data = deal_data(my_data,0,1)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist", con_divlist)
    print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    DM = Matrix_construct(con_data,pos_list,con_divlist)
