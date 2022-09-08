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
    filename = "Forest type mapping.csv"
    list_data = readfileBylist("target/" + filename)
    print(len(list_data),"对象数")
    print(len(list_data[0])-3,"条件属性数")
    con_data = list(map(lambda x: x[:(len(list_data[0]) - 1)], list_data))
    attr_all_set = []
    for i in range(len(con_data[0])):
        attr_set = set()
        for j in range(len(con_data)):
            if con_data[j][i] == '?':
                continue
            attr_set.add(int(con_data[j][i]))
        attr_all_set.append(attr_set)
    # ratio = int((len(con_data) * len(con_data[0])) * 0.05)

    #随机缺失
    ratio = int((len(con_data) * len(con_data[0])) * 0.10)
    print(ratio,"ratio",len(con_data) * len(con_data[0]))
    for i in range(ratio):
        attr_num = random.randint(0,len(con_data[0])-1)
        list_data[random.randint(0,len(con_data) - 1)][attr_num] = attr_all_set[attr_num]

    #本身缺失
    # for i in range(len(con_data[0])):
    #     for j in range(len(con_data)):
    #         if  con_data[j][i] == '?':
    #             list_data[j][i] = attr_all_set[i]

    with open("../set_value_datasets/10%/" + filename, 'w') as f:
        for i in range(len(list_data)):
            for j in range(len(list_data[0])):
                if j < len(con_data[0]):
                    if isinstance(list_data[i][j],set):
                        f.write(repr(list_data[i][j]) + "\t")
                    else:
                        f.write("{" + list_data[i][j] + "}" + "\t")
                elif j != len(con_data[0]) - 1:
                    f.write(list_data[i][j] + "\t")
                else:
                    f.write(list_data[i][j])
            if i != len(con_data)-1:
                f.write("\n")
    f.close()