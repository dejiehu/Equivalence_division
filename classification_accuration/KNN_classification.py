import numpy
from numpy import array
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from itertools import chain

def readfile(filename):#读文件
    my_data = numpy.loadtxt(filename)
    print(my_data)
    print("my_data.shape:",my_data.shape)
    return my_data

def deal_data(my_data,m,n):#处理数据表
    if n + 1 > m:
        for d in range(n,m-1,-1):
            my_data= numpy.delete(my_data,d,1)#d为下标
    return my_data


my_data = readfile("../complete_dataSet_classication/lymph.txt")
print(my_data)
X = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
y = deal_data(my_data, 0, my_data.shape[1] - 2).flatten()

# print(con_data)
print(y)

knn = KNeighborsClassifier(3)
# print (cross_val_score(knn, train, test, cv=3, scoring='accuracy').mean())
scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
# print(sum(scores))
sum = 0
for i in range(len(scores)):
    sum = sum + scores[i]
print("accury = ",sum/10)





