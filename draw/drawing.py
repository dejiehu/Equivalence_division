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

def draw_three(x,y,y1,y2):
    plt.plot(x, y, marker='o',color = 'b', mec='b', mfc='b',label='first floor')
    plt.plot(x, y1, marker='*', color = 'r',ms=10,  label='second floor')
    plt.plot(x, y2, marker='v', color='g', ms=10, label='thrid floor')
    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

def draw_four(x,y,y1,y2,y3):
    plt.plot(x, y3, marker='^', color='c', ms=10, label='all classes(K=4)')
    plt.plot(x, y, marker='o',color = 'r',label='single class(K=4)')
    plt.plot(x, y1, marker='*', color = 'b',ms=10,  label='single class(K=8)')
    plt.plot(x, y2, marker='v', color='g', ms=10, label='single class(K=16)')

    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

def Histogram(tick_label,y,y1,y2,y3):   #并列柱状图
    x =  np.arange(len(tick_label))
    bar_width = 0.2
    plt.bar(x, y, bar_width, align="center", color="c", label="all classes(K=4)", alpha=0.5)
    x = x + bar_width
    plt.bar(x, y1, bar_width, color="b", align="center", label="single class(K=4)", alpha=0.5)
    x = x + bar_width
    plt.bar(x , y2, bar_width, color="g", align="center", label="single class(K=8)", alpha=0.5)
    x = x + bar_width
    plt.bar(x, y3, bar_width, color="r", align="center", label="single class(K=16)", alpha=0.5)
    plt.xlabel("Size of universe")
    plt.ylabel("差别项个数")
    plt.xticks(x + bar_width / 2, tick_label)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    tick_label = ["A", "B", "C", "D", "E"]
    y = [6, 10, 4, 5, 1]
    y1 = [2, 6, 3, 8, 5]
    Histogram(tick_label, y, y1)
