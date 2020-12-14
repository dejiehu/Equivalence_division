import numpy
# numpy.set_printoptions(threshold=10000000000,linewidth =  8888)
def readfile():#读文件
    my_data = numpy.loadtxt('../zoo.txt')
    # my_data = numpy.loadtxt('Airfoil Self-Noise.txt')
    print(my_data)
    print("my_data.shape:",my_data.shape)
    return my_data

def Matrix_construct(my_data):  #构造矩阵
    s = set()
    DM = numpy.zeros(shape=(len(my_data), len(my_data)), dtype = tuple)
    for i in range(len(DM)):
        DM[i] = None
    for i in range(my_data.shape[0]):
        for j in range(i):
            s.clear()
            for k in range(my_data.shape[1]):
                if(my_data[i][k] != my_data[j][k]):
                    s.add(k)
            DM[i][j] = s.copy()
    print(DM)
    return DM

if __name__ == '__main__':
    my_data = readfile()
    DM = Matrix_construct(my_data)