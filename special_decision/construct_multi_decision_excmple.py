import time
from itertools import product

import numpy
from sklearn.cluster import KMeans
import pandas as pd

'''
正域保持约简
'''
from part2.quote_file import div
from draw .drawing import draw,draw_Compare

def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        s=[]
        for j in range(len(list_line) - 1):
            s.append(int(list_line[j]))
        s.append(float(list_line[len(list_line) - 1]))
        list_data.append(s)
    return list_data


def find_divlist(K,y_pred,old_dec_divlist):  #根据聚类结果找出dec_divlist
    dec_divlist = [[]] * K
    for i in range(len(y_pred)):
        dec_divlist[y_pred[i]] = dec_divlist[y_pred[i]] + [old_dec_divlist[i]]
    return dec_divlist

def dec_value(i,dec_data):   #判断划分的决策类中的值是否相等
    value = dec_data[i[0]]
    for j in i:
        if dec_data[j] != value:
            return False
    return True


def dec_divTwice(dec_divlist,dec_data):   #将决策进行二划分
    new_dec_divlist = []
    for i in dec_divlist:
        new_decSet = []
        if len(i) > 1:
            if dec_value(i,dec_data):
                new_dec_divlist += [i]
                continue
            for j in i:
                new_decSet.append(dec_data[j])
            # print("new_decSet",new_decSet)
            y_pred = KMeans(n_clusters=2, max_iter=300000).fit_predict(new_decSet)
            new_dec_divlist += find_divlist(2, y_pred, i)
        else:
            new_dec_divlist += [i]
    return new_dec_divlist

def add_newDec(con_data,dec_divlist):     #新决策添加到数据集
    for i in range(len(dec_divlist)):
        for j in dec_divlist[i]:
            con_data[j].append(i)
    # print(con_data)

if __name__ == '__main__':
    # start = time.perf_counter()
    # list_data = readfileBylist("../complete_dataSet_classication/german.txt")
    filename = "test2.csv"
    list_data = readfileBylist("../Numerical_decision_dataSet/" + filename)

    print(len(list_data),"对象数")
    print(len(list_data[0])-1,"条件属性数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    # print(dec_data)
    # print(con_data)
    K=2
    y_pred = KMeans(n_clusters=K, max_iter=300000).fit_predict(dec_data)
    # print(y_pred, "划分结果",len(y_pred),(type(y_pred)))
    dec_divlist = [[]] * K
    for i in range(len(y_pred)):
        dec_divlist[y_pred[i]] = dec_divlist[y_pred[i]] + [i]
    add_newDec(con_data, dec_divlist)
    print(dec_divlist)
    dec_divlist = dec_divTwice(dec_divlist, dec_data)
    add_newDec(con_data, dec_divlist)
    print(dec_divlist)
    dec_divlist = dec_divTwice(dec_divlist, dec_data)
    print(dec_divlist)
    print("最后聚了：",len(dec_divlist))
    add_newDec(con_data, dec_divlist)

    # array = numpy.array(con_data)
    # save = pd.DataFrame(array)
    # save.to_csv('multi_dataSet_Numerical/' + filename, index=False, header=False, sep="\t")



