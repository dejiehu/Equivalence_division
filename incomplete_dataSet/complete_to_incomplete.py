import random


def readfileBylist(filename):
    file = open(filename,"r")
    list_row = file.readlines()
    list_data = []
    for i in range(len(list_row)):
        list_line = list_row[i].strip().split('\t')
        list_data.append(list_line)
    return list_data

if __name__ == '__main__':
    list_data = readfileBylist("../zoo.txt")
    print(len(list_data),"对象数")
    print(len(list_data[0])-1,"条件属性数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    dec_data = list(map(lambda x: x[(len(list_data[0]) - 1):], list_data))
    ratio = int((len(list_data) * len(con_data[0])) * 0.1)
    print(ratio,"ratio",len(list_data) * len(con_data[0]))
    for i in range(ratio):
        list_data[random.randint(0,len(list_data)-1)][random.randint(0,len(con_data[0])-1)] = '?'
    with open('zoo_incomplete.txt', 'w') as f:
        for i in range(len(list_data)):
            for j in range(len(list_data[i])):
                if j != len(con_data[0]):
                    f.write(list_data[i][j]+",")
                else:
                    f.write(list_data[i][j])
            if i != len(con_data)-1:
                f.write("\n")
    f.close()