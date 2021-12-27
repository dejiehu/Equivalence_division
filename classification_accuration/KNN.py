# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import cross_val_score
# import numpy as np
# from sklearn.model_selection import KFold,StratifiedKFold
#
# X=np.array([
#     [1,2,3,4],
#     [11,12,13,14],
#     [21,22,23,24],
#     [31,32,33,34],
#     [41,42,43,44],
#     [51,52,53,54],
#     [61,62,63,64],
#     [71,72,73,74]
# ])
#
# y=np.array([1,1,0,0,1,1,0,0])
# floder = KFold(n_splits=5,random_state=0,shuffle=True)
# sfolder = StratifiedKFold(n_splits=4,random_state=0,shuffle=True)
#
# # for train, test in sfolder.split(X,y):
# #     print('Train: %s | test: %s' % (train, test))
# #     print(" ")
#
# # for train, test in floder.split(X,y):
# #     print('Train: %s | test: %s' % (train, test))
# knn = KNeighborsClassifier(n_neighbors=5)
# # 这里的cross_val_score将交叉验证的整个过程连接起来，不用再进行手动的分割数据
# # cv参数用于规定将原始数据分成多少份
# scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
# print(scores)
# print(scores.mean())

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
# import warnings
# warnings.filterwarnings("ignore")
from sklearn.model_selection import cross_val_score

data = load_iris()
# print(data)
train = data.data
print(train,"train",type(train))
test = data.target
print(test)
knn = KNeighborsClassifier(3)
print (cross_val_score(knn, train, test, cv=10, scoring='accuracy').mean())
scores = cross_val_score(knn, train, test, cv=10, scoring='accuracy')
print(sum(scores))

sum = 0
for i in range(len(scores)):
    sum = sum + scores[i]
print(sum/10)


