import copy
import random
import time
from itertools import chain
import numpy

shape_0 = 1000
shape_1 = 1000
start1 = time.perf_counter()
list1 = []
# print(len(list1))
for i in range(shape_0):
    list2 = []
    for j in range(0,shape_1):
        list2 += [random.randint(1,10)]
    list1.append(list2)
# print(list1)
a = 0
# for i in list1:
#     for k in list1:
#         if i == k:
#             print(i)
#             a+=1

# for i in list1:
#     for j in i:
#         for k in list1:
#             for l in k:
#                 if j == l:
#                     a += 1
# print(a)
con_data1 =[list1[i][:] for i in range(len(list1))]
# con_data1 = copy.deepcopy(list1)
end1 = time.perf_counter()
print("time1:",end1 - start1)

start2 = time.perf_counter()
core_data = numpy.empty(shape=(10,10))
# print(core_data)
for i in range((core_data.shape[0])):
    for j in range((core_data.shape[1])):
        core_data[i][j] = random.randint(1,10)
# print(core_data)
a = 0
# for i in range((core_data.shape[0])):
#     for j in range((core_data.shape[0])):
#         if (core_data[i] == core_data[j]).all():
#             a+=1
for i in range((core_data.shape[0])):
    for j in range((core_data.shape[1])):
        for k in range((core_data.shape[0])):
            for l in range((core_data.shape[1])):
                if core_data[i][j] == core_data[k][l]:
                    a += 1

# div_list = [[1,2,4,5,7,6,8,2,8,1,6,8,1,6]]
# for i  in range(2000):
    # list(chain.from_iterable(div_list))
end2 = time.perf_counter()
print("time2:",end2 - start2)

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split(' ')
        s = [int(j) for j in list_line]
        list_data.append(s)
    return list_data
list_data = readfileBylist("../complete_dataSet_classication/data.txt")
print(list_data)
del list_data[0][0]
print(list_data)
end3 = time.perf_counter()
print(end3-end2,"time")
def readfile1():
    my_data = numpy.loadtxt('../letter.txt')
    # print(my_data)
    m = my_data.tolist()
    return my_data
readfile1()
end4 = time.perf_counter()
print(end4-end3)
# print(readfile1("../data.txt"),"0000")
# if readfile("../Car Evaluation.txt")[1] == readfile1()[1]:
#     print("==")