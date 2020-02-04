# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os



datasetgostos = pd.read_csv("Gostou.csv")
datasetmedio = pd.read_csv("mais_ou_menos.csv")
datasetnega = pd.read_csv("nao_gostou.csv")

datanp = np.asarray(datasetgostos, dtype = list)
data = np.zeros((40863,140),dtype = int)


datanpmedio = np.asarray(datasetmedio, dtype = list)

datanpnega = np.asarray(datasetnega, dtype = list)

for i in range(data.shape[0]):
    data[i][0] = i + 1

for i in range(datanp.shape[0]):
    id = datanp[i][0]
    gostos = datanp[i][1].split(',')
    for k in range(len(gostos)):
        if (int(gostos[k]) > 0):
            data[id - 1][int(gostos[k])] = 3
   

for i in range(datanpmedio.shape[0]):  
    id = datanpmedio[i][0]
    medio = datanpmedio[i][1].split(',')      
    for k in range(len(medio)):
        if (int(medio[k]) > 0):
            data[id-1][int(medio[k])] = 2
for i in range(len(datanpnega)):
    id = datanpnega[i][0]
    negas = datanpnega[i][1].split(',') 
    for k in range(len(negas)):
        if(int(negas[k]) > 0):
            data[id-1][int(negas[k])] = 1

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if(data[i][j] == 0):
            data[i][j] = -99
                
#np.savetxt(os.getcwd(),data)
#np.savetxt(os.getcwd() + '\\data.txt',data, fmt='%i')