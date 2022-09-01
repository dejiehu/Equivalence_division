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
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y, marker='^', color='c', ms=10, label='PRDM')
    plt.plot(x, y1, marker='o', color='r', label='CSPRDM d1')
    plt.plot(x, y2, marker='*', color='b', ms=10, label='CSPRDM d2')
    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()


def draw_four_universe(x,y,y1,y2,y3):

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y3, marker='^', color='c', ms=10, label='PRDM')
    plt.plot(x, y, marker='o',color = 'r',label='CSPRDM d1')
    plt.plot(x, y1, marker='*', color = 'b',ms=10,  label='CSPRDM d2')
    plt.plot(x, y2, marker='v', color='g', ms=10, label='CSPRDM d3')

    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

def draw_four_attribute(x,y,y1,y2,y3):

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y3, marker='^', color='c', ms=10, label='PRDM')
    plt.plot(x, y, marker='o',color = 'r',label='CSPRDM d1')
    plt.plot(x, y1, marker='*', color = 'b',ms=10,  label='CSPRDM d2')
    plt.plot(x, y2, marker='v', color='g', ms=10, label='CSPRDM d3')

    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of attribute") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

# def Histogram(tick_label,y,y1,y2,y3):   #并列柱状图
#     x =  np.arange(len(tick_label))
#     bar_width = 0.2
#     plt.bar(x, y, bar_width, align="center", color="c", label="all classes(K=4)", alpha=0.5)
#     x = x + bar_width
#     plt.bar(x, y1, bar_width, color="b", align="center", label="single class(K=4)", alpha=0.5)
#     x = x + bar_width
#     plt.bar(x , y2, bar_width, color="g", align="center", label="single class(K=8)", alpha=0.5)
#     x = x + bar_width
#     plt.bar(x, y3, bar_width, color="r", align="center", label="single class(K=16)", alpha=0.5)
#     plt.xlabel("Size of universe")
#     plt.ylabel("差别项个数")
#     plt.xticks(x + bar_width / 4, tick_label)
#     plt.legend()
#     plt.show()

def Histogram():  # 并列柱状图
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    y=[70.2,18.3,70.0,42.4,44.9,50.8]
    y1=[28.8,0.7,26.2,3.7,5.5,10.7]
    y2=[7.4,0.3,12.8,2.8,0.9,2.7]
    y3=[1.9,0.3,1.1,0.9,0.9,0.09]
    tick_label = ["CST", "FF", "GWP", "CH", "IS(200)", "IS(2000)"]
    x = np.arange(len(tick_label))   # 横坐标范围
    total_width, n = 0.8, 4  # 柱状图总宽度，有几组数据
    width = total_width / n  # 单个柱状图的宽度
    x1 = x - width*1.5  # 第一组数据柱状图横坐标起始位置
    x2 = x1 + width  # 第二组数据柱状图横坐标起始位置
    x3 = x2 + width
    x4 = x3 + width

    plt.bar(x1, y, width = width,  color="c", label="PRDM", alpha=0.5)
    plt.bar(x2, y1, width = width, color="b", align="center", label="CSPRDM d1", alpha=0.5)
    plt.bar(x3, y2, width = width, color="g", align="center", label="CSPRDM d2", alpha=0.5)
    plt.bar(x4, y3, width = width, color="r", align="center", label="CSPRDM d3", alpha=0.5)
    plt.xlabel("Size of universe")
    plt.ylabel("Number of disjunctions(%)")
    plt.xticks(x , tick_label)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    Histogram()