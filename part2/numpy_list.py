import random
import time
from itertools import chain
import numpy
shape_0 = 100
shape_1 = 10
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
for i in list1:
    for k in list1:
        if i == k:
            print(i)
            a+=1
# for i in list1:
#     for j in i:
#         for k in list1:
#             for l in k:
#                 if j == l:
#                     a += 1
end1 = time.perf_counter()
print("time1:",end1 - start1)

start2 = time.perf_counter()
core_data = numpy.empty(shape=(100,10))
# print(core_data)
for i in range((core_data.shape[0])):
    for j in range((core_data.shape[1])):
        core_data[i][j] = random.randint(1,10)
# print(core_data)
a = 0
for i in range((core_data.shape[0])):
    for j in range((core_data.shape[0])):
        if (core_data[i] == core_data[j]).all():
            a+=1
# for i in range((core_data.shape[0])):
#     for j in range((core_data.shape[1])):
#         for k in range((core_data.shape[0])):
#             for l in range((core_data.shape[1])):
#                 if core_data[i][j] == core_data[k][l]:
#                     a += 1

# div_list = [[1,2,4,5,7,6,8,2,8,1,6,8,1,6]]
# for i  in range(2000):
    # list(chain.from_iterable(div_list))
end2 = time.perf_counter()
print("time2:",end2 - start2)