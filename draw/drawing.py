from matplotlib import pyplot as plt
from pylab import *                #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']


def draw(x,y):
    # x = range(len(names))
    plt.plot(x, y, marker='o',color = 'b', mec='b', mfc='b',label='all classes')
    # plt.plot(x, y1, marker='*', color = 'r',ms=10,  label=u'y=x^3曲线图')
    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

def draw_Compare(x,y,y1):
    plt.plot(x, y, marker='o',color = 'b', mec='b', mfc='b',label='all classes')
    plt.plot(x, y1, marker='*', color = 'r',ms=10,  label='single class')
    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()