'''
liang熵 正域加速
'''
import time
from itertools import chain
import numpy

def readfile():
    my_data = numpy.loadtxt('../data.txt')
    print(my_data)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

def del_dup(con_data,core_data):#删除重复列
    i = 0
    j = 0
    while i < core_data.shape[1]:
        while j < con_data.shape[1]:
            if (core_data[:, i] == con_data[:, j]).all():
                con_data = deal_data(con_data, j, j)
                continue
            j += 1
        i += 1
    return con_data

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

def divByUi(my_data,Ui): #1.数据表，2、3.删除元素下表   求划分集合
    divlist =[]#返回的划分集合
    list = []
    jump = 1
    for i in Ui:  # 8行
        list.clear()
        for l in range(len(divlist)):
            if (divlist[l].__contains__(i)):
                jump = 0
                break
        if jump == 0:
            jump = 1
            continue
        list.append(i)
        for j in Ui:
            if j == i:
                continue
            if ((my_data[i] == my_data[j]).all()):
                list.append(j)
        divlist.append(list.copy())
    return divlist

def L_Entropy(con_divlist,dec_divlist):  #梁的熵
    U_num = 0
    U = list(chain.from_iterable(con_divlist))
    l_entropy = 0
    for i in con_divlist:
        U_num += len(i)
    for i in con_divlist:
        for j in dec_divlist:
            i_c = (set(U).difference(set(i)))   #补集
            j_c = (set(U).difference(set(j)))   #补集
            if (len((set(i) & set(j))) != 0) & (len(i_c & j_c) != 0):
                l_entropy += (((len((set(i) & set(j)))/U_num) * (len(i_c & j_c))/U_num))
    return l_entropy

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    return  pos_list

def core(con_data, dec_divlist,l_entropy):  #基于条件熵求核
    core_data = numpy.empty(shape=(con_data.shape[0],0))
    for i in range(con_data.shape[1]):
        temp_con_data = deal_data(con_data,i,i)
        temp_con_divlist = div(temp_con_data)
        print("l_entr",L_Entropy(temp_con_divlist, dec_divlist))
        if l_entropy != (L_Entropy(temp_con_divlist, dec_divlist)):
            print("核属性是第",i,"个")
            core_data = numpy.append(core_data, con_data[:, i,numpy.newaxis], axis=1)
    return core_data


def Red(C0_data,dec_divlist,con_data,attr_data,L_Entropy):    #约简
    U = [i for i in range(con_data.shape[0])]
    Ui = U
    if C0_data.size == 0:
        return "无约简"
    B = C0_data
    dict = {}
    if L_Entropy(div(C0_data),dec_divlist) == L_Entropy:
        print("约简为",C0_data)
    else:
        while  L_Entropy(divByUi(con_data,Ui),dec_divlist) != L_Entropy(divByUi(B,Ui),dec_divlist):
            print("while",L_Entropy(divByUi(con_data,Ui),dec_divlist) , L_Entropy(divByUi(B,Ui),dec_divlist))
            dict.clear()
            con_key = -1  # 字典key
            con_value = 10000000  # 字典value
            pos_list = pos(dec_divlist, div(B))
            m = len(Ui) - 1
            while m >= 0:
                if set(pos_list).__contains__(Ui[m]):  # 删除对象
                    del Ui[m]
                m -= 1
            for i in range(attr_data.shape[1]):
                temp_C0_data = B
                temp_C0_data = numpy.append(temp_C0_data,attr_data[:,i,numpy.newaxis],axis=1)
                dict[i] = L_Entropy(divByUi(temp_C0_data,Ui),dec_divlist)
            print(dict)
            for key in dict:
                if dict[key] < con_value:
                    con_value = dict[key]
                    con_key = key
            B = numpy.append(B,attr_data[:,con_key,numpy.newaxis],axis=1)
            attr_data = deal_data(attr_data,con_key,con_key)
    return  B

def print_red(my_data,Red_data):
    red_set =[]
    for i in range(Red_data.shape[1]):
        for j in range( my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    print(set(red_set))

if __name__ == '__main__':
    # start = time.perf_counter()
    my_data = readfile()
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist",con_divlist)
    print("dec_divlist", dec_divlist)
    l_entropy = L_Entropy(con_divlist,dec_divlist)
    print("liang熵：",l_entropy)
    C0_data = core(con_data, dec_divlist,l_entropy)
    attr_data = del_dup(con_data,C0_data) #C-C0
    print_red(my_data, Red(C0_data,dec_divlist,con_data,attr_data,L_Entropy))
    # end = time.perf_counter()
    # print(end - start)