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

def div(my_data,m,n): #1.数据表，2、3.删除元素下表   求划分集合
    divlist =[]#返回的划分集合
    list = []
    jump = 1
    my_data= deal_data(my_data,m,n)#d为下标
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
    print("divlist ",divlist)
    return divlist

def pos(dec_divlist,con_divlist):  #子集
    pos_list=[]
    for i in dec_divlist:
         for j in con_divlist:
            if set(j).issubset(i):
                pos_list +=j
    return  pos_list

def dependency(pos_list,my_data):#正域
     dep_num =  (len(pos_list)/my_data.shape[0])
     print("依赖度:",dep_num)
     return dep_num

def core(my_data,dec_divlist,dep_num):#核
    my_data1 = deal_data(my_data,3,4)
    print(my_data1)
    print(my_data)
    for i in range(my_data1.shape[1]):
        temp_con_divlist = div(my_data1,i,i)
        pos_list = pos(dec_divlist, temp_con_divlist)
        if dep_num != dependency(pos_list,my_data):
            print("第",i,"个属性为核属性")

if __name__ == "__main__":
    my_data = readfile()
    con_divlist = div(my_data,3,4)
    dec_divlist = div(my_data,0,2)
    pos_list = pos(dec_divlist,con_divlist)
    print(pos_list,"pos_list")
    dep_num = dependency(pos_list,my_data)
    print(dep_num,"依赖度")
    core(my_data, dec_divlist,dep_num)
