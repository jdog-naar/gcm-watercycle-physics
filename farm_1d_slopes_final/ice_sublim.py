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

path_save = str(os.environ['path_save'])
name = str(os.environ['name'])

start_time = time.time()

saveformat = ".png"
#saveformat = ".pdf"


time_opendataset = time.time()
data = Dataset("diagfi.nc")

day_step = 48
rate = 24
day_init = 900 * day_step
nb_day = 195

iday = day_step*nb_day
day_end = day_init + iday

# =============================================================================
# Trucs de Lucas 
# =============================================================================
plt.rcParams.update({'font.size': 16})
plt.rcParams['axes.linewidth'] = 2 # set the value globally
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['xtick.minor.size'] = 1 #4
plt.rcParams['xtick.minor.width'] = 1.5
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['ytick.minor.size'] = 4
plt.rcParams['ytick.minor.width'] = 1.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.top'] = True
plt.rcParams['xtick.minor.top'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.major.pad'] = 6
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.pad'] = 6


xticks = np.linspace(100,101,13)
xlabels = np.linspace(0,24,13,dtype=int)

time = data.variables['Time'][day_init:day_end:rate]
tsurf = data.variables['tsurf'][day_init:day_end:rate]
tf = data.variables['tsurf'][day_init:day_end]
ice = data.variables['h2o_ice_s'][day_init:day_end:rate]

#tsmax = np.max(tf)
print(np.shape(tf),np.max(tf))
print("maximum temperature :",np.max(tf))
day_fully_sub = np.where(ice<1e-5)[0][0]
#print("maximum surface temperature : " + np.max(tf))
print("day of ice disappearance : " + str(day_fully_sub*abs(rate/day_step)))
print("name of figure is : " + path_save + "icerate"+name+saveformat)

fig,ax = plt.subplots(2,1,figsize = (14,12),sharex=True)

#ax2.margins(2, 2)           # Values >0.0 zoom out
ax[0].plot(time,tsurf,c='b')
ax[0].set_ylabel('Surface temperature (K)')
#ax[0,0].set_xticks(xticks)
#ax[0,0].set_xticklabels(xlabels)
ax[0].set_xlim(900,1100)

ax[1].plot(time,ice-ice[0],c='b')
ax[1].set_ylabel('Surface ice variation (kg/m2)')
ax[1].set_xlabel('Sol')
ax[1].vlines(time[day_fully_sub],ymin=-50,ymax=0,label=str(time[day_fully_sub]),ls='--')
#ax[0,1].set_xticks(xticks)
#ax[0,1].set_xticklabels(xlabels)
ax[1].set_xlim(900,1100)
ax[1].legend()
#ax2.set_title('Surface temperature')

#ax[1,0].plot(time,ice,c='b')
#ax[1,0].set_ylabel('Surface water ice (kg/m2)')
#ax[1,0].set_xlabel('Sol')
#ax[0,0].set_xticks(xticks)
#ax[0,0].set_xticklabels(xlabels)
#ax[1,0].set_xlim(900,1100)

plt.tight_layout()
#plt.savefig("lh_comp.pdf")




plt.savefig(path_save + "icerate"+name+saveformat)
#plt.show()
plt.close()


#print("Program done ! This took me %6.4f seconds" % (time.time() - start_time))
