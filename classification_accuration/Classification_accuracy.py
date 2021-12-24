import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

context = np.loadtxt("../Numerical_dataSet/seeds_dataset.txt")
rows, cols = context.shape

# attributes = [i for i in range(cols-1)]
attributes = [3, 4, 12, 10, 9, 8, 7, 5, 6]
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
    target.append(context[i][cols-1])
classes = len(list(set(target)))
print("class nums", classes)
train = np.array(data)
test = target.copy()
svc = SVC(kernel='rbf', probability=True)  # svm分类器
knn = KNeighborsClassifier(classes)

scores = cross_val_score(svc, train, test, cv=10, scoring='accuracy')
print(scores)
average_scores = sum(scores)/10
print("average accuracy", average_scores * 100, "%")
