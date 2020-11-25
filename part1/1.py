import time
import numpy

def readfile():
    my_data = numpy.loadtxt('../data.txt')
    print(my_data)
    return my_data

def div(my_data):
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
    print(div_list)

start = time.perf_counter()
my_data = readfile()
div(my_data)
end = time.perf_counter()
print(end - start)