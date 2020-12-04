import time
from itertools import chain

import numpy

def readfile():
    my_data = numpy.loadtxt('../data.txt')
    print(my_data)
    return my_data

def div(my_data):
    div_list = []
    list1= []
    for i in range(len(my_data)):
        list1.clear()
        if list(chain.from_iterable(div_list)).__contains__(i):    #展开
            continue
        list1.append(i)
        for j in range(i+1,len(my_data)):
            if((my_data[i] == my_data[j]).all()):
                list1.append(j)
        div_list.append(list1.copy())
    print(div_list)

if __name__ == '__main__':
    start = time.perf_counter()
    my_data = readfile()
    div(my_data)
    end = time.perf_counter()
    print(end - start)