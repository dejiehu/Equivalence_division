import numpy as np
import pandas as pd
import sympy as sy
from sympy.abc import *
if __name__ == '__main__':
    # filename = 'complete_dataSet_classication/data.txt'
    # rsnp = np.loadtxt(filename)
    # rspd = pd.DataFrame(rsnp, columns=list('abcde'))
    # print(type(rsnp))
    # aa = rspd.groupby(['a','b','c','d','e'])
    # # print(aa)
    # list1 = []
    # i=0
    # while i< len(aa):
    #     list1.append(list(aa)[i][1].index.tolist())
    #     # print(list(aa)[i][1].index,"   index")
    #     # print(list(aa)[i][1].index.tolist)
    #     i=i+1
    # print(list1)
    letter_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    list_attr = [{12}, {5}, {9, 2, 3}]
    formula = ""
    # print(len(list_attr[0]))
    for i in range(len(list_attr)):
        formula += ("(")
        for j in range(len(list_attr[i])):
            formula += ((letter_list[list(list_attr[i])[j]]))
            if j < len(list_attr[i]) - 1:
                formula += ("|")
            else:
                formula += (")")
        if i < len(list_attr) - 1:
            formula += ("&")
    print(formula)
    disjunctive_normal = sy.to_dnf(formula, True)
    disjunctive_normal = str(disjunctive_normal)
    disjunctive_normal = disjunctive_normal.replace('(','')
    disjunctive_normal = disjunctive_normal.replace(')', '')
    disjunctive_normal = disjunctive_normal.replace('&', '')
    disjunctive_normal = disjunctive_normal.replace(' ', '')
    print(disjunctive_normal)
    red_list = []
    red = []
    for i in disjunctive_normal:
        if i == '|':
            red_list.append(red)
            red = []
            continue
        red.append(letter_list.index(i))
    red_list.append(red)
    print(red_list)