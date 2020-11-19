import numpy

def readfile():#读文件
    my_data = numpy.loadtxt('zoo.txt')
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
    core_data = numpy.empty(shape=(con_data.shape[0],0))
    for i in range(con_data.shape[1]):
        temp_con_data = deal_data(con_data,i,i)
        temp_con_divlist = div(temp_con_data)
        pos_list = pos(dec_divlist, temp_con_divlist)
        if dep_num != dependency(pos_list,con_data):
            print("第",i,"个属性为核属性")
            core_data = numpy.append(core_data,con_data[:,i,numpy.newaxis],axis=1)
    return core_data

def Red(con_data,dec_divlist,core_data,dep_num):#约简
    core_list = div(core_data)
    core_dep = dependency(pos(dec_divlist,core_list),con_data)
    print("和属性依赖度：",core_dep)
    i = 0
    j = 0
    while i < core_data.shape[1]:
        while j < con_data.shape[1]:
            if (core_data[:,i] ==con_data[:,j]).all():
                con_data = deal_data(con_data,j,j)
                continue
            j = j + 1
        i = i + 1
    Red_data = core_data
    Red_dep = core_dep
    dict = {}#字典存放添加的依赖度
    num = 0
    while Red_dep != dep_num:
        # print("第",num,"次循环了")
        num += 1
        dict.clear()
        con_key = -1#字典key
        con_value = 0#字典value
        for k in range(con_data.shape[1]):
            temp_Red_data = Red_data
            temp_Red_data = numpy.append(temp_Red_data,con_data[:,k,numpy.newaxis],axis=1)
            Red_divlist = div(temp_Red_data)
            dict [k] = dependency(pos(dec_divlist,Red_divlist),con_data) - core_dep
        for key in dict:
            if con_value < dict[key]:
                con_value = dict[key]
                con_key = key
        Red_data = numpy.append(Red_data,con_data[:,con_key,numpy.newaxis],axis=1)
        con_data = deal_data(con_data,con_key,con_key)
        Red_dep = dependency(pos(dec_divlist, div(Red_data)), con_data)#添加条件属性后的依赖度
    return Red_data

def print_red(my_data,Red_data):
    red_set =[]
    for i in range(Red_data.shape[1]):
        for j in range( my_data.shape[1]):
            if (my_data[:, j] == Red_data[:, i]).all():
                red_set.append(j)
    return (red_set)

if __name__ == "__main__":
    my_data = readfile()
    con_data = deal_data(my_data,16,16)
    dec_data = deal_data(my_data,0,15)
    con_divlist = div(con_data)
    dec_divlist = div(dec_data)
    pos_list = pos(dec_divlist,con_divlist)
    dep_num = dependency(pos_list,my_data)
    core_data = core(con_data, dec_divlist,dep_num)
    print(print_red(my_data,Red(con_data,dec_divlist,core_data,dep_num)))

