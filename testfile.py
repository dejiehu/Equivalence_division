import itertools
import string
from itertools import product
#
# a = [1,2]
# b = [4,5,5]
# c = [6]
# loop_val = [a,b,c]
# for i in product(*loop_val):
#     print(i)



# for i in range(9):
#     print(i, "pre")
#     if i == 4:
#         print("跳出")
#         i = i+1
#         continue
#     print(i,"after")

#
# def get_DM(matrix):
#     table = pt.PrettyTable()
#     table.header = False
#     for i in range(len(matrix)):
#       table.add_row(matrix[i])
#     return table
#
# 执着的向日葵:
# for i in range(len(data[0])):
#     a.append(chr(97 + i))
# data.insert(0, a)


# list1 = []
# list1+= [0]
# list1+= [1]
# print(list1 == [0,1])


# import numpy as np
#
# a = np.array([[1, 3], [5, 7]])
# b = np.array([[2, 4], [6, 8]])
#
# c = np.append(a, b)
# d = np.append(a, b, axis=0)
# e = np.append(a, b, axis=1)
#
# print(a)
# print("c=\n", c)
# print("d=\n", d)
# print("e=\n", e)



# import numpy
#
# list1 = [1,2,3]
# list1 = [4,65,6]
# print(list1)
# R_data = numpy.empty(shape=(0,0))   #约简
# print(R_data.shape)




import time
# import numpy
#
# def readfile():
#     my_data = numpy.loadtxt('data.txt')
#     print(my_data)
#     new_data = numpy.empty(shape=(0,5))
#
#     print(my_data[range(0 , 4)].shape)
#     new_data = numpy.append(new_data,my_data[range(0,4)],axis=0)
#     print(new_data.shape)
#     # R_data = numpy.append(R_data, attr_data[:, n, numpy.newaxis], axis=1)
# readfile()


# loop_val = [{1,2},{1,3}]#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
#
# DM_list = []
# for i in product(*loop_val):
#     DM_list.append(set(i))
# print(DM_list)

#
# for i in itertools.combinations([0,5,7], 2):
#     DM_list.append(i)
# print(len(DM_list))

# import time
import numpy

# def readfile():
# my_data = numpy.loadtxt('data.txt')
# print((my_data[0] ==my_data[1]).all())
# i = [[0],[1],[2]]
# z=[[5]]
# for r in range(len(i)-1,-1,-1):
#     print(i[r])
#     if r == 1:
#         del i[r]
#         print("shanchu ")
# z.append(i+i)
# print(z)

# dict = {"1":4,"2":2,"3":6}
# print(dict)
# dict = sorted(dict.items(), key=lambda d:d[1],reverse= True)
# print(dict)
a=[[1,2,3],[1,9]]
b=[]
b = b+a
print(b)
# del dict[0]
# print(dict)
# print(dict[0][1])
# for i in dict:
#     print(i)
#     print(i[0])
#     print(i[1])
# my_data = numpy.loadtxt('incomplete_table1.txt')
# p = [1,2,5,'*','*']
# if p[3] == p[4]:
#     print("y")
# else:
#     print('N')
# print(my_data)

# a  = [[1,2,4,5],[5,8,9,6]]
# f = open("incomplete_table.txt", "r", encoding='utf-8')
#
# lines = f.readlines()  # 读取全部内容
#
# for i in range(0, lines.__len__(), 1):  # (开始/左边界, 结束/右边界, 步长)
#
#     list = []  ## 空列表, 将第i行数据存入list中
#     for word in lines[i].split():
#         word = word.strip()
#         list.append(word);
#     a.append(list)

# a  = [[1,2,4,5],[5
# sett = set()
# sett.add(1)
# sett.add(11)
# print(sett)