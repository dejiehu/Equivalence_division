import numpy
from numpy import array
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from itertools import chain
# numpy.set_printoptions(threshold=numpy.inf)

from sklearn.svm import SVC


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

def Classification_accuracy(filename,attr_list = None):
    my_data = readfile(filename)
    if attr_list == None:
        X = deal_data(my_data, my_data.shape[1] - 1, my_data.shape[1] - 1)
    else:
        X = numpy.empty(shape=(my_data.shape[0], 0))
        for i in attr_list:
            X = numpy.append(X, my_data[:, i, numpy.newaxis], axis=1)
    print(X)


    y = deal_data(my_data, 0, my_data.shape[1] - 2).flatten()

    knn = KNeighborsClassifier(3)

    # print (cross_val_score(knn, train, test, cv=3, scoring='accuracy').mean())
    scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
    sum = 0
    for i in range(len(scores)):
        sum = sum + scores[i]
    print("KNN accury = ",sum/10)


    svc = SVC(kernel='rbf', probability=True)  # svm分类器
    scores = cross_val_score(svc, X, y, cv=10, scoring='accuracy')
    sum = 0
    for i in range(len(scores)):
        sum = sum + scores[i]
    print("SVM accury = ",sum/10)


if __name__ == '__main__':
    Classification_accuracy("../complete_dataSet_classication/lymph.txt")

