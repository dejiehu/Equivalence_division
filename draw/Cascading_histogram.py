import matplotlib.pyplot as plt
import numpy as np



total_width, n = 0.8, 2
width = total_width / n
x = np.arange(4)
x_labels = ['BIO','FIT','YEA','CAR']
plt.xticks(x,x_labels)
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# 重新构建2的时间
yall21 = np.array([0.582959292,0.5952621250000001,2.0092964579999997,2.612290584])
yall22 = np.array([0.456890166,0.22637704199999975,1.0492766249999992,3.396174792])
# 细粒度2的差别矩阵和约简时间
y21 = np.array([0.08538250000000014,0.03585020799999983,0.10231645799999889,0.44817262499999977])
y22 = np.array([0.455662625,0.22687379200000013,1.0737975840000011,3.494078457999999])


plt.bar(x ,yall22,bottom=yall21,width=width,label="Get red",color='#CEEE8E')#合取析取（重新构造）
plt.bar(x,yall21,width=width,label="Make matrix classically",color='#D8BFD8',hatch='......')
plt.bar(x + width ,y22,bottom=y21,width=width,label="Get red",color='#00C9A6')
plt.bar(x + width ,y21,width=width,label="Make matrix dynamically",color='#B65494',hatch='......')


plt.legend()
plt.ylabel('Running time(s)')
plt.show()

