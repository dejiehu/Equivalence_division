import time

if __name__ == '__main__':
    i = 0
    s = time.perf_counter()
    dec_data = [0, 1, 1, 3, 4, 5, 4, 3, 4, 5, 67, 8, 89, 9, 8, 67, 5, 4, 6, 7, 8, 7, 6, 5, 4, 7, 8, 8, 7, 5, 4, 8, 7, 6,
                56]
    while(i < 100000):
        if dec_data.__contains__(77):
        # if  77 in dec_data:
            print(2)
        i += 1
    print(time.perf_counter54() - s)
