import operator
import numpy as np
import pandas as pd

###weka离散化后，字符转数字

# def readFile(filename):
#     data = []
#     try:
#         file = open(filename, 'r')
#     except Exception:
#         print("Error: 没有找到文件或读取文件失败")
#         return None
#         pass
#     else:
#         file_data = file.readlines()
#         i=0
#         for row in file_data:
#
#
#
#             tmp_list = row.split('\t')
#             tmp_list[-1] = tmp_list[-1].replace('\n', '')  # 去掉换行符
#             data.append(tmp_list)
#         return data

#数据处理
if __name__ == "__main__":
    filename = "auto-mpg.csv"
    # data = readFile( filename)#data里面已经不包括第一行
    # print(data)
    DM_list = [{5}, {1, 4}]
    obj = len(DM_list)
    attr = 5    #----------改动--------
    A = [[0 for i in range(attr)] for i in range(obj)]
    data = [[i for i in range(attr)]]
    data = data + A

    print(data)

    for i in range(len(DM_list)):
        for j in DM_list[i]:
            data[i+1][j-1] = 1


    # for i in range(len(data) - 1, -1, -1):
    #     if data[i][25] == '?':
    #         del data[i]
    #         continue
    array = np.array(data)
    save = pd.DataFrame(array)
    save.to_csv(filename, index=False, header=False, sep=" ")

    # DM_list = [{1,3},{1,2,4},{1,4,8},{1,2,9},{3,7,12},{3,6,13},{2,5},{4,10},{11}]  test.txt
    # DM_list = [{2,3,4,5}, {4,5,7,8,} ,{1,4,7,9}, {1,2,3,8}, {2,3,7,8}, {1,7,8}, {1,4,5}, {3,4,5,7}, {1,3,7}, {2,3,5,7}, {1,4,5,8}, {1,2,3,9}, {3,7,8,9}, {1,2,5,8,9}, {1,3,4,8,9},{6},{2,5,7,8,9},{1,2,4,7},{2,3,4,8},{1,3,5}]
    # DM_list = [{5},{1,4}] set_speed.txt
    # DM_list = [{3}, {5}, {6}, {4}, {2}]    #auto-mpg.csv
    # DM_list = [{3}, {2}, {6}, {7}, {8, 9}, {8, 1}, {1, 4}, {1, 9}, {8, 4}]  #Breast Tissue.csv
    # DM_list = [{11}, {23}, {22}, {3}, {20}, {1}, {2}, {19}, {10}, {16, 15}, {16, 17, 18, 24}]  # Chronic_Kidney_Disease.csv
    # DM_list = [{6}, {23}, {16}, {28}, {1}, {24}, {5, 7}, {12, 13}, {17, 7}, {10, 5}, {9, 13}, {2, 7}, {2, 13, 5}, {17, 4, 5}, {17, 11, 22}, {8, 9, 5}, {10, 11, 22}, {27, 2, 10}, {2, 12, 22}, {8, 11, 7}, {18, 27, 5}, {3, 4, 5}, {8, 2, 12, 5}, {9, 3, 22, 7}, {8, 17, 20, 5}, {8, 27, 2, 11}, {18, 27, 4, 20}, {8, 13, 5, 14}, {2, 27, 5, 14}, {8, 27, 11, 5}, {8, 12, 14, 7}, {17, 27, 4, 22}, {27, 11, 12, 5}, {27, 18, 11, 12}, {18, 27, 12, 7}, {17, 8, 25, 14, 15}, {7, 8, 25, 10, 27}, {17, 5, 8, 11, 14}, {7, 8, 25, 10, 13}, {17, 5, 27, 11, 15}, {8, 9, 10, 11, 27}, {2, 18, 5, 8, 11}, {17, 2, 5, 9, 27, 15}, {20, 7, 8, 9, 27, 12}, {3, 4, 8, 9, 11, 17, 26, 27}]
    # #Concrete Compressive Strength.csv
    # DM_list = [{9}, {6}, {3}, {8, 4}, {8, 10}, {1, 4}, {8, 1}, {8, 11}, {12, 5}, {2, 4, 12}, {1, 10, 5}, {10, 11, 4, 5}] #hcv
    # DM_list = [{12}, {5}, {8}, {11}, {1, 10}, {3, 4}, {4, 7}, {9, 7}, {1, 4}, {1, 3}, {2, 13}, {10, 13}, {4, 13}, {2, 4},
    #  {1, 13, 9}, {10, 4, 6}, {9, 10, 4}, {1, 2, 7}, {10, 2, 3}]
    # DM_list = [{5}, {17}, {2}, {4}, {16}, {12}, {15}, {1}, {18, 19}, {18, 7}, {10, 6}, {8, 6, 7}, {9, 10, 11, 7}]