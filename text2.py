import numpy as np
import pandas as pd

if __name__ == '__main__':
    filename = 'complete_dataSet_classication/data.txt'
    rsnp = np.loadtxt(filename)
    rspd = pd.DataFrame(rsnp, columns=list('abcde'))
    print(type(rsnp))
    aa = rspd.groupby(['a','b','c','d','e'])
    # print(aa)
    list1 = []
    i=0
    while i< len(aa):
        list1.append(list(aa)[i][1].index.tolist())
        # print(list(aa)[i][1].index,"   index")
        # print(list(aa)[i][1].index.tolist)
        i=i+1
    print(list1)
