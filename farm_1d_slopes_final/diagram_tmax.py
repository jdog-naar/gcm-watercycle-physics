#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 01:55:03 2022

@author: skywalker
"""

import numpy as np
from math import *
#import xarray as xr
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from jdog_style import *

print("beginning python program")

path_save = str(os.environ['path_save'])
#name = str(os.environ['name'])
simulist = os.environ['SIMULIST'].split("\n")

start_time = time.time()

#saveformat = ".png"
saveformat = ".pdf"
saveformat2 = ".png"


list_params = ['lh', 'alb_cap', 'alb_frost', 'atm_wat', 'ndt', 'lat', 'alb_bg','ti_bg','u','wc']

print(simulist)
print(np.array(simulist))
print(np.shape(np.array(simulist)))

tmax = np.zeros(np.shape(np.array(simulist)))
ice_day = np.zeros(np.shape(np.array(simulist)))
for i in range(len(np.array(simulist))):
    data = Dataset(np.array(simulist)[i]+"/diagfi.nc")
    day_step = 48
    rate = 1
    day_init = 900 * day_step
    nb_day = 195
    iday = day_step*nb_day
    day_end = day_init + iday
    time = data.variables['Time'][day_init:day_end:rate]
    tf = data.variables['tsurf'][day_init:day_end:rate]
    ice = data.variables['h2o_ice_s'][day_init:day_end:rate]
    try:
        day_fully_sub = np.where(ice<1e-6)[0][0]
    except IndexError:
        day_fully_sub = 200*day_step
    print("Number of simu :", i)
    print("day_fully_sub :", day_fully_sub)
    ice_day[i] = day_fully_sub*abs(rate/day_step)
    tmax[i] = np.max(tf[:day_fully_sub])
    print("local iceday :", day_fully_sub*abs(rate/day_step))
    print("local tmax :", np.max(tf[:day_fully_sub]))


index = np.genfromtxt("indexarray.txt", delimiter=' ')


ftlegend=14
###############
### Default ###
###############
scat = []

fig,ax = plt.subplots(1,1,figsize = (12,7),sharex=True)
ax.hlines(273.15,xmin=0,xmax=100,color='k',ls='--',alpha=0.4)
ax.annotate('273.15 K : melting',(50,274),alpha=0.4)
ax.annotate('temperature of water',(50,271.5),alpha=0.4)
for i in range(len(index[:,0])):
    if (index[i,0]==1.0): ### chaleur latente
        ecolor='b'
    if (index[i,0]==2.0):
        ecolor='r'
    if (index[i,2]==1.0): ### albedo
        fcolor = "grey"
    if (index[i,2]==2.0): ### albedo
        fcolor = "None"
    if (index[i,2]==3.0):
        fcolor = 'black'
    if (index[i,7]==1.0): ### inertie thermique
        size=300
    if (index[i,7]==2.0):
        size=1100
    if (index[i,8]==1.0): ### vent zonal
        mark='s'
    if (index[i,8]==2.0):
        mark='^'
    if (index[i,8]==3.0):
        mark='o'
    scat.append(ax.scatter(np.squeeze(ice_day[i]),np.squeeze(tmax)[i],facecolor=fcolor,edgecolor=ecolor,marker=mark,s=size,linewidth=5))
ax.set_xlabel('Day of ice disappearance (sol)')
ax.set_ylabel('Maximum surface temperature (K)')
ro1 = ax.scatter(1,1,facecolor="None",edgecolor='r',marker='o',s=300,linewidth=5)
bo1 = ax.scatter(1,1,facecolor="None",edgecolor='b',marker='o',s=300,linewidth=5)
bo2 = ax.scatter(1,1,facecolor="None",edgecolor='b',marker='o',s=1100,linewidth=5)
bo3 = ax.scatter(1,1,facecolor="grey",edgecolor='b',marker='o',s=300,linewidth=5)
bo4 = ax.scatter(1,1,facecolor="black",edgecolor='b',marker='o',s=300,linewidth=5)
bt1 = ax.scatter(1,1,facecolor="None",edgecolor='b',marker='^',s=300,linewidth=5)
bs1 = ax.scatter(1,1,facecolor="None",edgecolor='b',marker='s',s=300,linewidth=5)
titre= ax.scatter(1,1,facecolor="None",edgecolor='b',marker='s',s=0,linewidth=0)
ax.set_xlim((0,73))
ax.set_ylim((245,277))
print(np.shape(scat))
plt.savefig(path_save + "diagram_tmax_noleg"+saveformat,bbox_inches="tight")
ax.set_xlabel('Day of ice disappearance (sol)')
#ax.legend([scat[0],scat[2],scat[4],scat[5],scat[6]], ["Latent Heat", "THI", "Wind speed", "Albedo",""],markerfirst=False,ncol=3)
l1 = plt.legend([titre]+[ro1,bo1],["Latent heat"]+ ["False", "True"],markerfirst=True,ncol=3,loc='upper left',bbox_to_anchor=(1.02, 1),frameon=False,labelspacing=0.5)
l2 = plt.legend([titre]+[bo1,bo2], ["Thermal Inertia"]+["240", "400"],markerfirst=True,ncol=3,loc='upper left',bbox_to_anchor=(1.02, 0.75),frameon=False, labelspacing=0.5)
ll1 = plt.legend([titre,titre,ro1,bo1,bo1,bo2],["Latent heat","Thermal Inertia","False","240", "True", "400"],markerfirst=True,ncol=3,loc='upper left',bbox_to_anchor=(-0.1, -0.12),frameon=False,labelspacing=0.8, handletextpad=0.5,fontsize=ftlegend)
l3 = plt.legend([titre]+[bo1,bo3,bo4],["Albedo"]+ ["0.4", "0.35", "0.3"],markerfirst=True,ncol=4,loc='upper left',bbox_to_anchor=(1.02, 0.5),frameon=False, labelspacing=0.5)
#l4 = plt.legend([bo1,bt1,bs1], ["2.5", "5", "10"],markerfirst=True,ncol=3,title="wind (m.s$^{-1}$)")
l4 = plt.legend([titre]+[bo1,bt1,bs1],["Wind (m.s$^{-1}$)"]+ ["10", "5", "2.5"],markerfirst=True,ncol=4,loc='upper left',bbox_to_anchor=(1.02, 0.25),frameon=False, labelspacing=0.5)
ll2 = plt.legend([titre]+[titre]+[bo1,bo1,bo3,bt1,bo4,bs1],["Ice albedo"]+["Wind (m.s$^{-1}$)"]+ ["0.4","10", "0.35", "5", "0.3", "2.5"],markerfirst=True,ncol=4,loc='upper left',bbox_to_anchor=(0.4, -0.12),frameon=False, labelspacing=0.8, handletextpad=0.5,fontsize=ftlegend)
ax=plt.gca()
#ax.add_artist(l1)
#ax.add_artist(l2)
#ax.add_artist(l3)
#ax.add_artist(l4)
ax.add_artist(ll1)
ax.add_artist(ll2)
#plt.tight_layout()
plt.savefig(path_save + "diagram_tmax"+saveformat,bbox_inches="tight")
plt.savefig(path_save + "diagram_tmax"+saveformat2,bbox_inches="tight")
plt.close()

handles1, labels1 = l1.legendHandles, l1.get_texts()
handles2, labels2 = l2.legendHandles, l2.get_texts()
handles3, labels3 = l3.legendHandles, l3.get_texts()
handles4, labels4 = l4.legendHandles, l4.get_texts()

# Sauvegarde de chaque légende séparément


print("Program done !")
