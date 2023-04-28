from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
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

def draw_two_universe(x,y,y1):
    # plt.plot(x, y3, marker='^', color='#1874CD', ms=9, label='PRDM')
    # plt.plot(x, y, marker='o', color='#FFCC33', label='CSPRDM $d^3$')
    # plt.plot(x, y1, marker='o', color='#66FF00', label='CSPRDM $d^2$')
    # plt.plot(x, y2, marker='o', color='#FF6666', label='CSPRDM $d^1$')
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y, marker='^', color='#99CCFF', ms=9, label='Reconstruct')
    plt.plot(x, y1, marker='o',color = '#FF6666',label='Dynamic update')
    # plt.plot(x, y1, marker='o', color = '#66FF00', label='CSPRDM $d^2$')
    # plt.plot(x, y2, marker='o', color='#FF6666',  label='CSPRDM $d^1$')

    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()


# #广义决策特定类
# def draw_three_universe(x,y,y1,y2):
#     plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
#     plt.plot(x, y, marker='^', color='c', ms=10, label='MRGDM')
#     plt.plot(x, y1, marker='o', color='r', label='MRSGDM(class:1;value:0)')
#     plt.plot(x, y2, marker='*', color='b', ms=10, label='MRSGDM(class:1,2;value:0,3)')
#     plt.legend()  # 让图例生效
#     # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
#     plt.margins(0)  #据边缘的距离
#     plt.subplots_adjust(bottom=0.2)
#     plt.xlabel("Size of universe") #X轴标签
#     plt.ylabel("Time consumption(s)") #Y轴标签
#     # plt.title("A simple plot") #标题
#     plt.show()

#广义决策特定类  开放刊
def draw_four_universe_two(x,y,y1):
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替

    plt.plot(x, y, marker='^', color='#1874CD', label='GRM')
    plt.plot(x, y1, marker='o', color='#FF6666', label='SGRM')

    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

#广义决策特定类 开放刊
def draw_four_attribute_two(x,y,y1):
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替

    plt.plot(x, y, marker='^', color='#1874CD',  label='GRM')
    plt.plot(x, y1, marker='o', color='#FF6666',label='SGRM')

    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of attribute") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()
#广义决策特定类
def draw_four_universe_g(x,y,y1,y2,y_pos,name):
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y_pos, marker='*', color='#996633', label='PRM')
    plt.plot(x, y, marker='^', color='#1874CD', label='GRM')
    plt.plot(x, y1, marker='o', color='#FF6666', label='SGRM')
    plt.plot(x, y2, marker='o', color='#66FF00',  label='MGRM')
    plt.legend(fontsize=15)  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.xlabel("Size of universe",fontsize=18) #X轴标签
    plt.ylabel("Time consumption(s)",fontsize=18) #Y轴标签
    # plt.title("A simple plot") #标题
    plt.savefig("universe/" + name + ".jpg", dpi=230)
    plt.show()

#广义决策特定类
def draw_four_attribute_g(x,y,y1,y2,y_pos,name):
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替



    plt.plot(x, y_pos, marker='*', color='#996633', label="PRM")

    plt.plot(x, y, marker='^', color='#1874CD',  label='GRM')
    plt.plot(x, y1, marker='o', color='#FF6666',label='SGRM')
    plt.plot(x, y2, marker='o', color='#66FF00',  label='MGRM')
    plt.legend(fontsize=15)  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    # my_x_ticks = np.arange(2, len(x) + 1, 2)
    # plt.xticks(my_x_ticks, fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of attribute",fontsize=18) #X轴标签
    plt.ylabel("Time consumption(s)",fontsize=18) #Y轴标签
    # plt.title("A simple plot") #标题
    plt.savefig("attribute/" + name + ".jpg", dpi=230)
    plt.show()

#广义决策特定类
def draw_three_universe(x,y,y1,y2):
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y, marker='^', color='#1874CD', label='MRGDM')
    plt.plot(x, y1, marker='o', color='#FF6666', label='MRSGDM(class:1;value:0)')
    plt.plot(x, y2, marker='o', color='#66FF00',  label='MRMGDM(class:1,2;value:0,3)')
    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of universe") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

#广义决策特定类
def draw_three_attribute(x,y,y1,y2):
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y, marker='^', color='#1874CD',  label='MRGDM')
    plt.plot(x, y1, marker='o', color='#FF6666',label='MRSGDM(class:1;value:0)')
    plt.plot(x, y2, marker='o', color='#66FF00',  label='MRMGDM(class:1,2;value:0,3)')
    plt.legend()  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.xlabel("Size of attribute") #X轴标签
    plt.ylabel("Time consumption(s)") #Y轴标签
    # plt.title("A simple plot") #标题
    plt.show()

# #广义决策特定类
# def draw_three_attribute(x,y,y1,y2):
#     plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
#     plt.plot(x, y, marker='^', color='c', ms=10, label='MRGDM')
#     plt.plot(x, y1, marker='o', color='r', label='MRSGDM(class:1;value:0)')
#     plt.plot(x, y2, marker='*', color='b', ms=10, label='MRSGDM(class:1,2;value:0,3)')
#     plt.legend()  # 让图例生效
#     # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
#     plt.margins(0)  #据边缘的距离
#     plt.subplots_adjust(bottom=0.2)
#     plt.xlabel("Size of attribute") #X轴标签
#     plt.ylabel("Time consumption(s)") #Y轴标签
#     # plt.title("A simple plot") #标题
#     plt.show()


def draw_four_universe(x,y,y1,y2,y3,name):

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    plt.plot(x, y3, marker='^', color='#1874CD', ms=9, label='PRM')
    plt.plot(x, y, marker='o',color = '#FFCC33',label='SPRM $d^3$')
    plt.plot(x, y1, marker='o', color = '#66FF00', label='SPRM $d^2$')
    plt.plot(x, y2, marker='o', color='#FF6666',  label='SPRM $d^1$')

    plt.legend(fontsize=15)  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.xlabel("Size of universe",fontsize=18) #X轴标签
    plt.ylabel("Time consumption(s)",fontsize=18) #Y轴标签
    # plt.title("A simple plot") #标题
    plt.savefig("universe/" + name + ".jpg",dpi = 230)
    plt.show()

def draw_four_attribute(x,y,y1,y2,y3,name):

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替

    plt.plot(x, y3, marker='^', color='#1874CD', ms=10, label='PRM')
    plt.plot(x, y, marker='o', color='#FFCC33', label='SPRM $d^3$')
    plt.plot(x, y1, marker='o', color='#66FF00',  label='SPRM $d^2$')
    plt.plot(x, y2, marker='o', color='#FF6666',  label='SPRM $d^1$')

    plt.legend(fontsize=15)  # 让图例生效
    # plt.xticks(x, names)   #轴刻度间隔   显示标签   标签字体倾斜度和颜色等外观属性
    plt.margins(0)  #据边缘的距离
    plt.subplots_adjust(bottom=0.2)
    plt.yticks(fontsize=15)
    # my_x_ticks = np.arange(1, len(x) + 1, 2)
    plt.xticks(fontsize=15)
    plt.xlabel("Size of attribute",fontsize=18) #X轴标签
    plt.ylabel("Time consumption(s)",fontsize=18) #Y轴标签
    # plt.title("A simple plot") #标题
    plt.savefig("attribute/"+ name + ".jpg", dpi=400)
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

def Histogram_1():  # 并列柱状图  正域
    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    y = [70.2, 18.3, 70.0, 42.4, 60.94, 68.54, 44.9, 50.8]
    y1 = [28.8, 0.7, 26.2, 3.7, 21.47, 14.71, 5.5, 10.7]
    y2 = [7.4, 0.3, 12.8, 2.8, 6.91, 2.89, 0.9, 2.7]
    y3 = [1.9, 0.3, 1.1, 0.9, 2.89, 0.26, 0.9, 0.09]
    tick_label = ["1", "2", "3", "4",
                  "5", "6", "7",
                  "8"]
    x = np.arange(len(tick_label))  # 横坐标范围

    total_width, n = 0.8, 4  # 柱状图总宽度，有几组数据
    width = total_width / n  # 单个柱状图的宽度
    x1 = x - width * 1.5  # 第一组数据柱状图横坐标起始位置
    x2 = x1 + width  # 第二组数据柱状图横坐标起始位置
    x3 = x2 + width
    x4 = x3 + width

    plt.bar(x1, y, width=width, color="c", label="PRM", alpha=0.5)
    plt.bar(x2, y1, width=width, color="b", align="center", label="SPRM $d^3$", alpha=0.5)
    plt.bar(x3, y2, width=width, color="g", align="center", label="SPRM $d^2$", alpha=0.5)
    plt.bar(x4, y3, width=width, color="r", align="center", label="SPRM $d^1$", alpha=0.5)
    plt.xlabel("Data sets")
    plt.ylabel("Number of disjunctions(%)")

    plt.yticks()
    plt.legend()
    # plt.xticks(x, tick_label, rotation=60)
    plt.xticks(x, tick_label)   #fontsize=15
    plt.legend()
    plt.savefig("正域.jpg", dpi=300)
    plt.show()


def auto_label(rects):
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def auto_text(rects):
    for rect in rects:
        plt.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom',fontsize = 6)

#广义决策特定类
def Histogram_2():  # 并列柱状图

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    y = [77.83,73.51,84.34,75.76,69.70,83.24,14.22,64.60]
    y1 = [1.63,11.46,3.30,15.88,8.03,4.28,0.29,9.98]
    y2 = [24.38,29.34,19.18,24.80,16.32,9.36,3.86,22.37]
    tick_label = ["1", "2", "3", "4",
                  "5", "6", "7",
                  "8"]
    x = np.arange(len(tick_label))  # 横坐标范围
    total_width, n = 0.72, 3  # 柱状图总宽度，有几组数据
    width = total_width / n  # 单个柱状图的宽度
    x1 = x - width * 1  # 第一组数据柱状图横坐标起始位置

    x3 = x1 + width
    x2 = x3 + width  # 第二组数据柱状图横坐标起始位置

    rects1 = plt.bar(x1, y, width=width, color="c", label="MRGDM", alpha=0.5)
    rects2 = plt.bar(x2, y1, width=width, color="r", align="center", label="MRSGDM", alpha=0.5)
    rects3 = plt.bar(x3, y2, width=width, color="b", align="center", label="MRMGDM", alpha=0.5)

    # for a,b in zip(x1,y):
    #     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize = 7)
    # for a,b in zip(x2,y):
    #     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize = 7)
    # for a,b in zip(x3,y):
    #     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize = 7)
    auto_text(rects1)
    auto_text(rects2)
    auto_text(rects3)
    plt.xlabel("Data sets")
    plt.ylabel("Number of disjunctions(%)")
    plt.xticks(x, tick_label)
    plt.legend()
    # plt.subplots_adjust(bottom=0.01)
    plt.savefig("测试1.png",dpi = 550)
    plt.show()

#广义决策特定类  开放刊
def Histogram_4():  # 并列柱状图

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替

    y1 = [77.83,73.51,84.34,75.76,69.70,83.24,14.22,64.60]
    y3 = [1.63,11.46,3.30,15.88,8.03,4.28,0.29,9.98]
    tick_label = ["1", "2", "3", "4",
                  "5", "6", "7",
                  "8"]
    x = np.arange(len(tick_label))  # 横坐标范围
    total_width, n = 0.8, 2  # 柱状图总宽度，有几组数据
    width = total_width / n  # 单个柱状图的宽度
    x2 = x - width * 0.5  # 第一组数据柱状图横坐标起始位置
    x4 = x2 + width  # 第二组数据柱状图横坐标起始位置
    rects2 = plt.bar(x2, y1, width=width, color="b", align="center", label="GRM", alpha=0.5)
    rects4 = plt.bar(x4, y3, width=width, color="r", align="center", label="SGRM", alpha=0.5)


    # 广义决策特定类  对比正域
def Histogram_3():  # 并列柱状图

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    y = [77.83, 75.24, 84.73, 75.87, 69.70, 77.02, 15.92, 66.91]
    y1 = [77.83, 73.51, 84.34, 75.76, 69.70, 83.24, 14.22, 64.60]
    y2 = [24.38, 29.34, 19.18, 24.80, 16.32, 9.36, 3.86, 22.37]
    y3 = [1.63, 11.46, 3.30, 15.88, 8.03, 4.28, 0.29, 9.98]
    tick_label = ["1", "2", "3", "4",
                  "5", "6", "7",
                  "8"]
    x = np.arange(len(tick_label))  # 横坐标范围
    total_width, n = 0.8, 4  # 柱状图总宽度，有几组数据
    width = total_width / n  # 单个柱状图的宽度
    x1 = x - width * 1.5  # 第一组数据柱状图横坐标起始位置
    x2 = x1 + width  # 第二组数据柱状图横坐标起始位置
    x3 = x2 + width
    x4 = x3 + width

    rects1 = plt.bar(x1, y, width=width, color="c", label="PRM", alpha=0.5)
    rects2 = plt.bar(x2, y1, width=width, color="b", align="center", label="GRM", alpha=0.5)
    rects3 = plt.bar(x3, y2, width=width, color="g", align="center", label="MGRM", alpha=0.5)
    rects4 = plt.bar(x4, y3, width=width, color="r", align="center", label="SGRM", alpha=0.5)

    plt.legend()  # 让图例生效
    # auto_text(rects1)
    # auto_text(rects2)
    # auto_text(rects3)
    # auto_text(rects4)
    plt.xlabel("Data sets")
    plt.ylabel("Number of disjunctions(%)")
    plt.xticks(x, tick_label)


    # plt.subplots_adjust(bottom=0.01)
    plt.ylim(0, 100)
    plt.savefig("广义决策.jpg", dpi=300)
    plt.show()


def Histogram_two():  # 并列柱状图

    plt.rcParams['font.sans-serif'] = 'times new roman'  # 设置全局字体，会被局部字体顶替
    y = [0.04,0.16,7.31,0.03,0.06,1.07,0.04,7.88]
    y1 = [0.05,0.19,25.32,0.10,0.16,2.15,0.07,20.98]
    # y2 = [24.38,29.34,19.18,24.80,16.32,9.36,3.86,22.37]
    tick_label = ["Concrete Slump Test", "Forest Fires", "Garments Worker Productivity", "Computer Hardware",
                  "Behavior of the urban traffic", "Dow Jones Index", "Image Segmentation(210)",
                  "Image Segmentation(2100)"]
    x = np.arange(len(tick_label))  # 横坐标范围
    total_width, n = 0.8, 2  # 柱状图总宽度，有几组数据
    width = total_width / n  # 单个柱状图的宽度
    x1 = x - width * 0.5  # 第一组数据柱状图横坐标起始位置

    x2 = x1 + width
    # x2 = x3 + width  # 第二组数据柱状图横坐标起始位置

    rects1 = plt.bar(x1, y, width=width, color="c", label="Dynamic update", alpha=0.5)
    rects2 = plt.bar(x2, y1, width=width, color="r", align="center", label="Reconstruct", alpha=0.5)
    # rects3 = plt.bar(x3, y2, width=width, color="b", align="center", label="MRMGDM", alpha=0.5)

    # for a,b in zip(x1,y):
    #     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize = 7)
    # for a,b in zip(x2,y):
    #     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize = 7)
    # for a,b in zip(x3,y):
    #     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize = 7)
    auto_text(rects1)
    auto_text(rects2)
    # auto_text(rects3)
    plt.xlabel("Data sets")
    plt.ylabel("Time consumption(s)")
    plt.xticks(x, tick_label)
    plt.legend()

    plt.xticks(x, tick_label, rotation=60)
    # plt.subplots_adjust(bottom=0.01)
    plt.savefig("测试1.png",dpi = 600)
    plt.show()

if __name__ == '__main__':
    # Histogram_two()
    # Histogram_1()
    # Histogram_3()
    # Histogram_3()
    # y = np.arange(1, 5)
    #
    # plt.plot(y, color='#FF6666')
    #
    # plt.plot(y + 1, color='#99FF66')  #
    #
    # plt.plot(y + 2, color='#FFCC33')
    #
    # plt.plot(y + 3, color='#1874CD')  #
    # plt.show()
    # my_x_ticks = np.arange(1, 14, 2)
    # print(my_x_ticks)
    #
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #
    # y3 = [3.809929525, 11.525238922999998, 31.06907609200001, 53.84949935500002, 73.91595766500001, 145.76914458099998, 199.224342966, 256.99392799200007, 358.6307506190001, 451.186457582]
    #
    # y =[1.0715569839999999, 3.1693335589999982, 6.073608542000002, 7.820675316000006, 10.916020332000016, 13.528953150000007, 15.304226184000072, 18.027116924999973, 81.60118568999997, 84.76826635799989]
    #
    # y1 =[1.1524370920000004, 3.022323141000001, 5.146993084999991, 7.708274278000005, 10.267823468000017, 13.017838691000009, 14.790495276000001, 17.54892251000001, 20.81969086999993, 23.728432971000075]
    #
    # y2 =[0.01684491099999974, 0.06807564600000049, 0.14029485300000033, 0.2587732340000173, 0.423741452999991, 0.6317559529999812, 0.7894286079999802, 1.505333563000022, 1.3313102199999776, 2.9672528450000755]
    #
    # name = "Image Segmentation(2100)"
    #
    # draw_four_universe(x, y, y1, y2, y3, name) #y3, 'PRM' ### y, 'SPRM $d^3$'###  y1  SPRM $d^2   ####   y2   SPRM $d^1$


    #
    # y3 =




    #
    # y =
    #
    # y1 =
    #
    # y2 =
    y3 =[1.821815762, 1.7778934809999782, 70.01803557999997, 76.22672030199999, 117.55060206799999, 128.07832721600005,
     163.11207792800008, 174.21193539399997, 193.4901237649999, 197.49891622099994, 272.6170648230004, 285.388608963,
     334.708105833, 333.60630436400015, 378.26839680199964, 390.09965479899984, 387.84485846000007, 405.3886929630007,
     419.9722790750002]
    y =[1.6314563969999938, 1.6864133600000173, 1.89020207599998, 1.6766071240000429, 1.679462682999997,
     1.6370106279999845, 2.0078946769999675, 2.0455471720001697, 2.0857174479999685, 2.1030450270000074,
     8.240364764999867, 7.383396065999932, 8.099061464999977, 8.512865573, 44.054296516999784, 52.239345208000486,
     55.23086030800005, 58.16853666900079, 82.63608351500079]
    y1 =[1.6289039499999944, 1.7013560460000008, 1.8942500820000419, 1.6629368839999756, 1.673166230999982,
     1.6250101670000276, 2.0455356159998246, 2.088417007000089, 2.2940675030001785, 2.1365899589998207,
     2.394764082000165, 2.1224188300002425, 2.2858528250003474, 2.1900269200000366, 2.4339228010003353,
     2.252515002999644, 2.581314109000232, 2.629896395999822, 21.99245465600052]
    y2 =[1.6369595160000046, 1.7182222910000178, 1.817076644999986, 1.6934102579999717, 1.6541679829999794,
     1.6465870849999646, 2.027769815000056, 2.021691583999882, 2.2182762909999383, 2.156518874999847, 2.366624932999912,
     2.1507126450001124, 2.265897243999916, 2.227671859000111, 2.4085440999997445, 2.2713688060002823,
     2.4647863979998874, 2.521811362000335, 2.95580127500034]

    x = [i for i in range(1, len(y3) + 1)]
    name = "Image Segmentation(2100)"

    draw_four_attribute(x,y,y1,y2,y3,name)


    # y =
    # y1 =
    # y2 =
    # y_pos =


    #
    # x = [i for i in range(1, len(y2) + 1)]
    # name = "auto-mpg.csv"
    #
    # draw_four_attribute_g(x, y, y1, y2, y_pos, name)

    # x = [i for i in range(1, len(y3) + 1)]
