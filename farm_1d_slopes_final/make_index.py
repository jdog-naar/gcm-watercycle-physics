"""
Created on Wed Nov  2 21:01:41 2022

@author: skywalker
"""

import numpy as np
import string
import os

tot_simus = int(os.environ['tot_simus'])
tot_params = int(os.environ['tot_params'])

params_tochange = np.array(list(os.environ["params_tochange"])) 
params_tochange = ' '.join(params_tochange).split()
params_tochange = np.array(params_tochange).astype(np.int)
params_tochange = params_tochange -1
nbparams = np.array(list(os.environ['nbparams']))
nbparams = ' '.join(nbparams).split()
nbparams = np.array(nbparams).astype(np.int)
index = np.ones((tot_simus,tot_params))
print(np.shape(index))
print(index)
print(params_tochange)
print(nbparams)
j=1
k=0
i=params_tochange[0]
for i in range(len(params_tochange)):
    test = np.delete(nbparams,k)
    print("j = ",j)
    print("k = ",k)
    print("nbparams[k] = ",nbparams[k])
    print("test = ",test)
    print("prod = ",np.prod(test))
    index[:,params_tochange[i]]=np.tile(np.repeat(np.arange(1,nbparams[k]+1),j),np.int((np.prod(test))/j))
    print(i)
    k=k+1
    j=j*nbparams[k-1]
print(index)
np.savetxt("indexarray.txt",index, fmt='%i', delimiter=' ')
