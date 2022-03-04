import scipy.io as scio

dataFile = "Bridges.mat"
data = scio.loadmat(dataFile)
print(type(data))
print (data)