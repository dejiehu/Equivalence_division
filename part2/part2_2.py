from itertools import product

import part2_1

def logic_operation(diffItem_list):#析取，吸收
    DM_list = []
    for i in diffItem_list:  #排序
        if len(DM_list) != 0:  # 列表不等0要找位置插入
            k = 0
            while k < len(DM_list):
                if len(set(i)) <= len(set(DM_list[k])):
                    DM_list.insert(k, i)
                    break
                k += 1
            if k == len(DM_list):
                DM_list.append(i)
        else:  # 列表为空直接加入
            DM_list.append(i)
    # print( len(DM_list),DM_list,"排序后集合")  #排序后集合

    m = len(DM_list) - 1# 吸收多余的集合
    while m > 0: #m从后往前
        n = 0  #从前往后
        while n < m:
            # print(DM_list[n],DM_list[m],DM_list[n].issubset(DM_list[m]))
            if set(DM_list[n]).issubset(DM_list[m]):
                del DM_list[m]
                m = len(DM_list)
                break
            n += 1
        m -= 1
    return DM_list

def Red(DM):#逻辑运算
    DM_list = []
    for i in range(DM.shape[0]):   #矩阵差别项放到集合DM_list中
        for j in range(i):
            if len(set(DM[i][j])) == 0:#把集合为空的丢掉
                continue
            DM_list.append(DM[i][j])
    DM_list = logic_operation(DM_list)#集合析取逻辑操作（多余集合被吸收）
    print(DM_list,"多余集合被吸收")
    loop_val = []#将合取式差分为析取式     loop_val = [{1,2},{1,3}]
    for i in DM_list:
        loop_val.append(i)
    DM_list = []
    for i in product(*loop_val):
        DM_list.append(set(i))
    DM_list = logic_operation(DM_list)
    print("约简的集合为：",DM_list)


if __name__ == '__main__':
    my_data = part2_1.readfile()
    DM = part2_1.Matrix_construct(my_data) #差别矩阵
    Red(DM)

