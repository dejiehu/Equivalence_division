import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

# context = np.loadtxt("../data/untolerance/Hepatitis.txt")
# rows, cols = context.shape
#
# # attributes = [i for i in range(cols-1)]
# attributes = [1, 2, 5, 8, 9, 10, 14, 15, 17]
# attributes = list(set(attributes))
# data = []
# target = []
# for i in range(rows):
#     temp = []
#     for j in range(len(attributes)):
#         p = attributes[j]
#         ret = context[i][p]
#         temp.append(ret)
#     data.append(temp.copy())
#     target.append(context[i][cols-1])
# classes = len(list(set(target)))
# print("class nums", classes)
# train = np.array(data)
# test = target.copy()
# svc = SVC(kernel='rbf', probability=True)  # svm分类器
# scores = cross_val_score(svc, train, test, cv=10, scoring='accuracy')
# print(scores)
# average_scores = sum(scores)/10
# print("svm average accuracy", average_scores * 100, "%")
#
#
# knn = KNeighborsClassifier(classes)
#
# scores = cross_val_score(knn, train, test, cv=10, scoring='accuracy')
# print(scores)
# average_scores = sum(scores)/10
# print("knn average accuracy", average_scores * 100, "%")
#
from Readfile.read_file import readFile


def get_accuracy(file, attributes):
    # context = np.loadtxt(file,delimiter=',')
    context = np.loadtxt(file)

    rows, cols = context.shape

    # attributes = [i for i in range(cols-1)]

    attributes = list(set(attributes))
    data = []
    target = []
    for i in range(rows):
        temp = []
        for j in range(len(attributes)):
            p = attributes[j]
            ret = context[i][p]
            temp.append(ret)
        data.append(temp.copy())
        target.append(context[i][cols - 1])
    classes = len(list(set(target)))
    print("class nums", classes)
    train = np.array(data)
    test = target.copy()
    svc = SVC(kernel='rbf', probability=True)  # svm分类器
    scores = cross_val_score(svc, train, test, cv=10, scoring='accuracy')
    # print(scores)
    svm_average_scores = sum(scores) / 10
    print("svm", '%.4f'%svm_average_scores)

    knn = KNeighborsClassifier(classes)#knn

    scores = cross_val_score(knn, train, test, cv=10, scoring='accuracy')
    # print(scores)
    knn_average_scores = sum(scores) / 10
    # print("knn average accuracy", average_scores * 100, "%")
    print("knn", '%.4f'%knn_average_scores)


    # gnb = GaussianNB()#高斯朴素贝叶斯
    # # clf = clf.fit(iris.data, iris.target)
    # # y_pred = clf.predict(iris.data)
    # scores = cross_val_score(gnb, train, test, cv=10, scoring='accuracy')
    # # print(scores)
    # gnb_average_scores = sum(scores) / 10
    # # print("knn average accuracy", average_scores * 100, "%")
    # print("高斯朴素贝叶斯", '%.4f' % gnb_average_scores)
    return svm_average_scores





if __name__ == "__main__":
    file="../data/tolerance/lung_cancer.txt"
    # context = np.loadtxt()
    attributes =[1,14,45,13,9,34]
    # data = readFile(file)
    print("svm",'%.4f'%get_accuracy(file,attributes))