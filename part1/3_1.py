import numpy

def readfile():#读文件
    my_data = numpy.loadtxt('data.txt')
    print(my_data)
    print("my_data.shape:",my_data.shape)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data

def div(my_data): #1.数据表，2、3.删除元素下表   求划分集合
    divlist =[]#返回的划分集合
    list = []
    jump = 1
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

def pos(dec_divlist,con_divlist):  #子集  正域集合
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    return  pos_list

def dependency(pos_list,my_data):#依赖度
     dep_num =  (len(pos_list)/my_data.shape[0])
     return dep_num

def core(con_data,dec_divlist,dep_num):# 根据 属性重要度  求核
    for i in range(con_data.shape[1]):
        temp_con_data = deal_data(con_data,i,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        print("单个属性依赖度：",dependency(pos_list,con_data))
        if dep_num != dependency(pos_list,con_data):
            print("第",i,"个属性为核属性")

if __name__ == "__main__":
    my_data = readfile()
    con_data = deal_data(my_data,4,4)
    dec_data = deal_data(my_data,0,3)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    pos_list = pos(dec_divlist,con_divlist)
    dep_num = dependency(pos_list,my_data)
    print("条件属性依赖度:", dep_num)
    core(con_data, dec_divlist,dep_num)
