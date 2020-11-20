import time
import numpy

def readfile():
    my_data = numpy.loadtxt('../zoo.txt')
    print(my_data)
    return my_data

def deal_data(my_data, m, n):  # 处理数据表
    if n + 1 > m:
        for d in range(n, m - 1, -1):
            my_data = numpy.delete(my_data, d, 1)  # d为下标
    return my_data
def Max_min(con_data):
    for i in




if __name__ == '__main__':
    my_data = readfile()
    con_data = deal_data(my_data,4,4)
    dec_data = deal_data(my_data,0,3)
