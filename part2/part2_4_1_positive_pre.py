import numpy
'''
正域保持约简
'''
# numpy.set_printoptions(suppress=True)
numpy.set_printoptions(threshold=10000000000,linewidth =  8888)
from itertools import product
def readfile():
    my_data = numpy.loadtxt('../traffic.txt')
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
    print(pos_list,"pos_list")
    return pos_list

def Matrix_construct(con_data,pos_list,con_divlist):  #构造基于正域的矩阵
    s = set()
    DM = numpy.zeros(shape=(len(con_data), len(con_data)), dtype = tuple)
    for i in range(len(DM)):
        DM[i] = None
    for i in range(con_data.shape[0]):
        for j in range(i):
            s.clear()
            index = 0
            for m in range(len(con_divlist)):
                if con_divlist[m].__contains__(i):
                    if set(con_divlist[m]).issubset(set(pos_list)):
                        # print(set(con_divlist[m]),set(pos_list),"子集")
                        break
                if m == len(con_divlist) - 1:
                    index = len(con_divlist) - 1
            if index == len(con_divlist) - 1:
                DM[i][j] = None
                continue
            for k in range(con_data.shape[1]):
                if(con_data[i][k] != con_data[j][k]):
                    s.add(k)
            DM[i][j] = s.copy()
    print(DM)
    return DM

def logic_operation(diffItem_list):#析取，吸收
    DM_list = []
    for i in diffItem_list:  #排序
        if len(DM_list) != 0:  # 列表不等0要找位置插入
            k = 0
            while k < len(DM_list):
                if len(set(i)) <= len(set(DM_list[k])):
                    DM_list.insert(k, i)
                    break
                k += 1
            if k == len(DM_list):
                DM_list.append(i)
        else:  # 列表为空直接加入
            DM_list.append(i)
    m = len(DM_list) - 1# 吸收多余的集合
    while m > 0: #m从后往前
        n = 0  #从前往后
        while n < m:
            # print(DM_list[n],DM_list[m],DM_list[n].issubset(DM_list[m]))
            if set(DM_list[n]).issubset(DM_list[m]):
                del DM_list[m]
                m = len(DM_list)
                break
            n += 1
        m -= 1
    return DM_list

def Red(DM):#逻辑运算
    DM_list = []
    for i in range(DM.shape[0]):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if DM[i][j] == None:#把集合为空的丢掉
                continue
            if len(DM[i][j]) == 0:
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    DM_list = []
    for i in product(*loop_val):
        DM_list.append(set(i))
    DM_list = logic_operation(DM_list)
    print("约简的集合为：",len(DM_list), DM_list)

if __name__ == '__main__':
    my_data = readfile()
    con_data = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    dec_data = deal_data(my_data, 0, my_data.shape[1] - 2)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    print("con_divlist", con_divlist)
    print("dec_divlist", dec_divlist)
    pos_list = pos(dec_divlist,con_divlist)
    DM = Matrix_construct(con_data,pos_list,con_divlist)
    Red(DM)