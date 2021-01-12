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


list1 = []
list1+= [0]
list1+= [1]
print(list1 == [0,1])
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