import copy
import math
import time


def readfile(file_name):#读文件
    my_data = []
    f = open(file_name, "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    for i in range(0, lines.__len__(), 1):  # (开始/左边界, 结束/右边界, 步长)
        list = []  ## 空列表, 将第i行数据存入list中
        for word in lines[i].split():
            word = word.strip()
            list.append(word)
        my_data.append(list)
    # print(my_data)
    return my_data

def deal_data(my_data,m,n):#选出条件属性和决策属性
    data = copy.deepcopy(my_data)
    if n + 1 > m:
        for d in range(n,m-1,-1):
            for i in range(len(data)):
                del data[i][d]
    return data

def cal_red_divlist(red_list,con_data):   #根据核属性数值计算核属性数据
    red_data = copy.deepcopy(con_data)
    for i in range(len(U_con_data[0])-1,-1,-1):
        if not red_list.__contains__(i):
            red_data = deal_data(red_data, i, i)
    return red_data

def del_dup(U_con_data,core_list):  #找出未被添加的属性c-c0
    attr_list = [i for i in range(len(U_con_data[0]))]
    j = len(U_con_data) - 1
    while j >= 0:
        if core_list.__contains__(j):
            U_con_data = deal_data(U_con_data,j, j)
            del attr_list[j]
        j -= 1
    return U_con_data,attr_list

def elements_add(list_1,list_2,i):  #元素增加
    temp_list = copy.deepcopy(list_1)
    for j in range(len(list_1)):
        temp_list[j].append(list_2[j][i])
    return temp_list

def  increasing_preference(U_con_data,i,j):  #求关系矩阵时用于判断
    if i == j:
        return True
    for k in range(len(U_con_data[0])):
        if U_con_data[i][k] > U_con_data[j][k]:
            return False
    return True

def dominance_relation_matrix(U_con_data): # 求关系矩阵
    matrix = []
    for i in range(len(U_con_data)):
        temp_matrix = []
        for j in range(len(U_con_data)):
            if increasing_preference(U_con_data,i,j):   #用于判断
                temp_matrix.append(1)
            else:
                temp_matrix.append(0)
        matrix.append(temp_matrix)
    return matrix

def  right_increasing_preference(U_con_data,Ux_con_data,i,j):  #求关系矩阵时用于判断
    for k in range(len(U_con_data[0])):
        if U_con_data[i][k] > Ux_con_data[j][k]:
            return False
    return True

def right_dominance_relation_matrix(U_con_data,Ux_con_data): # 增加时，求右侧关系矩阵
    matrix = []
    for i in range(len(U_con_data)):
        temp_matrix = []
        for j in range(len(Ux_con_data)):
            if right_increasing_preference(U_con_data,Ux_con_data,i,j):   #用于判断
                temp_matrix.append(1)
            else:
                temp_matrix.append(0)
        matrix.append(temp_matrix)
    return matrix

def  below_increasing_preference(U_con_data,Ux_con_data,i,j):  #求关系矩阵时用于判断
    if i == j - len(U_con_data):
        return True
    for k in range(len(U_con_data[0])):
        if j < len(U_con_data):
            if Ux_con_data[i][k] > U_con_data[j][k]:
                return False
        if j >= len(U_con_data):
            if Ux_con_data[i][k] > Ux_con_data[j - len(U_con_data)][k]:
                return False
    return True

def below_dominance_relation_matrix(U_con_data,Ux_con_data): # 增加时，求下侧关系矩阵
    matrix = []
    for i in range(len(Ux_con_data)):
        temp_matrix = []
        for j in range(len(U_con_data) + len(Ux_con_data)):
            if below_increasing_preference(U_con_data,Ux_con_data,i,j):   #用于判断
                temp_matrix.append(1)
            else:
                temp_matrix.append(0)
        matrix.append(temp_matrix)
    return matrix

def matrix_intersection(matrix_1,matrix_2):#矩阵求交集
    matrix = copy.deepcopy(matrix_1)
    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[0])):
            matrix[i][j] = matrix_1[i][j] * matrix_2[i][j]
    return matrix

def dominance_diagonal_matrix(matrix): #求对角矩阵   结果用list表示
    diagonal_matrix = []
    for i in matrix:
        diagonal_matrix.append(sum(i))
    return diagonal_matrix

def new_dominance_diagonal_matrix(original_matrix,right,below): #求新的对角矩阵   结果用list表示
    diagonal_matrix = dominance_diagonal_matrix(original_matrix)
    for i in range(len(diagonal_matrix)):
        diagonal_matrix[i] += sum(right[i])
    for j in range(len(below)):
        diagonal_matrix.append(sum(below[j]))
    return diagonal_matrix

def inverse_dominance_matrix(diagonal_matrix):   #求对角矩阵的逆矩阵
    inverse_matrix = diagonal_matrix.copy()
    for i in range(len(inverse_matrix)):
        inverse_matrix[i] = 1/inverse_matrix[i]
    return inverse_matrix

def matrix_combina(original,right,below):
    U_Ux_matrix = copy.deepcopy(original)
    for i in range(len(original)):
        U_Ux_matrix[i] += right[i]
    U_Ux_matrix += below
    return U_Ux_matrix


def new_MDCE(U_con_data,Ux_con_data,U_Ux_dec_matrix):
    U_con_matrix = dominance_relation_matrix(U_con_data)
    Ux_right_matrix =right_dominance_relation_matrix(U_con_data, Ux_con_data)
    Ux_below_matrix =below_dominance_relation_matrix(U_con_data, Ux_con_data)
    U_Ux_matrix = matrix_combina(U_con_matrix,Ux_right_matrix,Ux_below_matrix)
    U_Ux_d_matrix = matrix_intersection(U_Ux_matrix,U_Ux_dec_matrix)
    U_Ux_diagonal_matrix = new_dominance_diagonal_matrix(U_con_matrix,Ux_right_matrix,Ux_below_matrix)
    U_Ux_d_diagonal_matrix = dominance_diagonal_matrix(U_Ux_d_matrix)
    U_Ux_con_inverse_matrix = inverse_dominance_matrix(U_Ux_diagonal_matrix)
    sum = 1
    for i in range(len(U_Ux_con_inverse_matrix)):
        sum *= U_Ux_d_diagonal_matrix[i] * U_Ux_con_inverse_matrix[i]
    # print( - math.log2(sum) / len(U_Ux_d_diagonal_matrix),"return")
    return - math.log2(sum) / len(U_Ux_d_diagonal_matrix)

def RED(red_list,U_con_data,Ux_con_data,U_dec_data,Ux_dec_data):
    U_Ux_dec_matrix = dominance_relation_matrix(U_dec_data + Ux_dec_data)
    U_Ux_con_entropy = new_MDCE(U_con_data, Ux_con_data, U_Ux_dec_matrix)
    U_red_data = cal_red_divlist(red_list,U_con_data)
    Ux_red_data = cal_red_divlist(red_list, Ux_con_data)
    U_Ux_red_entropy = new_MDCE(U_red_data, Ux_red_data, U_Ux_dec_matrix)
    if U_Ux_red_entropy == U_Ux_con_entropy:
        de_redundancy(U_Ux_dec_matrix, red_list, U_red_data, Ux_red_data, U_Ux_con_entropy)
        return
    U_attr_data, attr_list = del_dup(U_con_data, red_list)
    Ux_attr_data, attr_list = del_dup(Ux_con_data, red_list)
    # print(attr_data)
    dict = {}
    for i in attr_list:
        U_temp_red_data = elements_add(U_red_data, U_attr_data, i)
        Ux_temp_red_data = elements_add(Ux_red_data, Ux_attr_data, i)
        dict[i] = U_Ux_red_entropy - new_MDCE(U_temp_red_data, Ux_temp_red_data, U_Ux_dec_matrix)
    dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    while U_Ux_con_entropy != U_Ux_red_entropy:
        red_list = red_list + [attr_list[dict[0][0]]]
        U_red_data = elements_add(U_red_data, U_attr_data, dict[0][0])
        Ux_red_data = elements_add(Ux_red_data, Ux_attr_data, dict[0][0])
        del dict[0]
        U_Ux_red_entropy = new_MDCE(U_red_data, Ux_red_data, U_Ux_dec_matrix)
    de_redundancy(U_Ux_dec_matrix, red_list, U_red_data, Ux_red_data, U_Ux_con_entropy)


def de_redundancy(U_Ux_dec_matrix,red_list,U_red_data,Ux_red_data,U_Ux_con_entropy):
    for i in range(len(red_list)-1,-1,-1):
        U_temp_red_data = deal_data(U_red_data,i,i)
        Ux_temp_red_data = deal_data(Ux_red_data, i, i)
        if  new_MDCE(U_temp_red_data, Ux_temp_red_data, U_Ux_dec_matrix) == U_Ux_con_entropy:
            U_red_data = deal_data(U_red_data, i, i)
            Ux_red_data = deal_data(Ux_red_data, i, i)
            del red_list[i]
    print(red_list)

if __name__ == '__main__':
    start = time.perf_counter()
    U_data = readfile("table.txt")
    Ux_data = readfile("add_data.txt")
    U_Ux_data = U_data + Ux_data
    print(U_data)
    print(Ux_data)
    print(U_Ux_data)
    U_con_data = deal_data(U_data, len(U_data[0]) - 1, len(U_data[0]) - 1)
    U_dec_data = deal_data(U_data, 0, len(U_data[0])  - 2)
    Ux_con_data = deal_data(Ux_data, len(Ux_data[0]) - 1, len(Ux_data[0]) - 1)
    Ux_dec_data = deal_data(Ux_data, 0, len(Ux_data[0]) - 2)
    red_list = [0,1,2]
    RED(red_list, U_con_data, Ux_con_data, U_dec_data, Ux_dec_data)