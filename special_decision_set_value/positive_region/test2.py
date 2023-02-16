import matplotlib.pyplot as plt
import numpy as np



total_width, n = 0.8, 2
width = total_width / n
x = np.arange(4)
x_labels = ['1','2','3','4']
plt.xticks(x,x_labels)
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# 重新构建2的时间
# yall21 = np.array([0.013,0.1082,4.032,5.0599])
# yall22 = np.array([0.0024,0.0549,0.1917,0.3514])
yall21 = np.array([0.0026,0.007422,0.005246,0.00814])
yall22 = np.array([0.00185,0.0028,0.00270,0.00546])
# 细粒度2的差别矩阵和约简时间
# y21 = np.array([0.0028,0.016,0.37,0.4240])
# y22 = np.array([0.0024,0.0672,0.1941,0.3010])
y21 = np.array([0.0013,0.0016,0.0008955,0.00014])
y22 = np.array([0.0022013,0.0025,0.00253,0.007015])


plt.bar(x ,yall22,bottom=yall21,width=width,label="Get red",color='#CEEE8E')#合取析取（重新构造）
plt.bar(x,yall21,width=width,label="Make matrix classically",color='#D8BFD8',hatch='......')
plt.bar(x + width ,y22,bottom=y21,width=width,label="Get red",color='#00C9A6')
plt.bar(x + width ,y21,width=width,label="Make matrix dynamically",color='#B65494',hatch='......')


plt.legend()
plt.ylabel('Running time(s)')
plt.show()

