# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 10:34:59 2020

@author: sjz
"""

## collection of data

import numpy as np
import matplotlib.pyplot as plt
import addcopyfighandler
# %%
# 5. 'three dipoles' - a large system consisting of 1000 molecules
# beta - Mex - et- anisotropy 
#bl = np.array([0, 1, 1])
#et_matrix = np.matrix([[1.0, 0.0, 0.0],
#                       [1.0, 0.0, 0.0],
#                       [1.0, 0.0, 0.0]])
#N_system = np.array([1000])

beta = np.array([0, 10, 20, 30, 40, 45])
beta_r = beta * np.pi / 180
Mex = np.array([1.00, 	0.93,	0.77,	0.50,	0.17,	0.00])
portrait_r0 = np.array([0.386,	0.351,	0.273,	0.148,	0.069,	0.009])
funnel_et = np.array([0.000,	0.060,	0.234,	0.501,	0.827,	1.000])
residue = np.array([0.001,	0.001,	0.001,	0.001,	0.000,	0.000])

# one y axis
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]}, sharex=True, figsize = (9, 5))

ax1.plot(Mex, funnel_et, 'ro-')
ax1.plot(Mex, portrait_r0, 'go-')
ax1.invert_xaxis()    
ax1.legend(['funnel et', 'portrait r'])

ax2.plot(Mex, residue,'ko-')
ax2.invert_xaxis() 
ax2.legend(['residue'], loc='upper left')
ax2.set_ylim([-0.02, 0.1])


# two y axis
fig, (ax1, ax3) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]}, sharex=True, figsize = (8.2, 6))

ax1.set_ylabel('anisotropy', color = 'g')  # we already handled the x-label with ax1
ax1.set_ylim(-0.285714, 0.40)
ax1.plot(Mex, portrait_r0, 'go-')
ax1.tick_params(axis='y', labelcolor='g')
ax1.legend(['portrait r', 'analytical r'], bbox_to_anchor=(-0.55, 0.3, 0.8, 0.5))

ax2 = ax1.twinx()  

ax2.set_ylabel('energy transfer efficiency', color='r')
ax2.plot(Mex, funnel_et, 'ro-')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim (0.0, 2.0)
ax2.legend(['funnel et', 'analytical et'], bbox_to_anchor=(-0.55, -0.2, 0.8, 0.5) ) 

ax3.plot(Mex, residue,'ko-')
ax3.legend(['residue'])
ax3.set_xlabel('Mex')
ax3.set_ylim([-0.01, 0.1])

ax1.invert_xaxis() 

# %%
# 4.'two dipoles' - a large system consisting of 1000 molecules
# beta - et- anisotropy 
# nReplicates = 1
# bl = np.array([1, 0])
# et_matrix = np.matrix([[0.0, 1.0],
#                       [0.0, 1.0]])
# N_system = np.array([1000])

# simulation data
beta_deg = np.linspace(0, 180, 19)
portrait_r0 = np.array([0.381,	0.352,	0.304,	0.175,	0.078,	-0.048,	-0.168,	-0.235,	-0.262,	-0.276,	-0.272,	-0.226,	-0.151,	-0.071,	0.080,	0.194,	0.265, 0.364, 0.406])
funnel_et = np.array([0.000,	0.061,	0.234,	0.499,	0.826,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	0.827,	0.500,	0.234, 0.06, 0.00])
residue = np.array([0.004,	0.005,	0.007,	0.007,	0.006,	0.016,	0.037,	0.056,	0.069,	0.074,	0.069,	0.056,	0.036,	0.014,	0.005,	0.006,	0.007,	0.007,	0.004])

# theoritical solution
beta_r = beta_deg * np.pi / 180

#r0 = 0.2 * (3 * np.cos(beta_r) **2 - 1)
r0 = (24.0 / 35.0) * np.cos(beta_r)**2 - (2.0 / 7.0)
et = (2 - 5 * r0)/(2 + r0)
# et [et>=1.0] = 1

fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]}, sharex=True, figsize = (9, 5))

ax1.plot(beta_deg[0:10], funnel_et[0:10], 'ro-')
ax1.plot(beta_deg[0:10], et[0:10], 'ro--')

ax1.plot(beta_deg[0:10], portrait_r0[0:10], 'go-')
ax1.plot(beta_deg[0:10], r0[0:10], 'go--')
ax1.legend(['funnel et', 'analytical et', 'portrait r', 'analytical r'])

ax2.plot(beta_deg[0:10], residue[0:10],'ko-')
ax2.legend(['residue'])
ax2.set_xlabel('\u03B2 (angle between two dipoles)')
ax2.set_ylim([-0.02, 0.1])


# two y axis
fig, (ax1, ax3) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]}, sharex=True, figsize = (8.2, 6))

ax1.set_ylabel('anisotropy', color = 'g')  # we already handled the x-label with ax1
ax1.set_ylim(-0.285714, 0.40)
ax1.plot(beta_deg[0:10], portrait_r0[0:10], 'go-')
ax1.plot(beta_deg[0:10], r0[0:10], 'g--')
ax1.tick_params(axis='y', labelcolor='g')
ax1.legend(['portrait r', 'analytical r'], bbox_to_anchor=(0.0, 0.35, 0.5, 0.5))

ax2 = ax1.twinx()  

ax2.set_ylabel('energy transfer efficiency', color='r')
ax2.plot(beta_deg[0:10], funnel_et[0:10], 'ro-')
ax2.plot(beta_deg[0:10], et[0:10], 'r--')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim (0.0, 2.0)
ax2.legend(['funnel et', 'analytical et'], bbox_to_anchor=(0.0, -0.2, 0.5, 0.5)) 


ax3.plot(beta_deg[0:10], residue[0:10],'ko-')
ax3.legend(['residue'])
ax3.set_xlabel('\u03B2 (angle between two dipoles)')
ax3.set_ylim([0.0, 0.1])

# %%
# 4.'two dipoles' - a large system consisting of 1000 molecules
# Epsilon is larger than 1
# beta - et- anisotropy 
# nReplicates = 1
# bl = np.array([1, 0])
# et_matrix = np.matrix([[0.0, 1.0],
#                       [0.0, 1.0]])
# N_system = np.array([1000])


beta_deg = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
portrait_r0 = np.array([0.405,	0.368,	0.292,	0.206,	0.066,	-0.040,	-0.170,	-0.245,	-0.273,	-0.286])
funnel_et = np.array([0.000,	0.060,	0.234,	0.499,	0.826,	1.173,	1.500,	1.767,	1.940,	2.000])
residue = np.array([0.002,	0.003,	0.001,	0.002,	0.001,	0,	0,	0.002,	0.002,	0.001])

# theoritical solution
beta_r = beta_deg * np.pi / 180

#r0 = 0.2 * (3 * np.cos(beta_r) **2 - 1)
r0 = (24.0 / 35.0) * np.cos(beta_r)**2 - (2.0 / 7.0)
et = (2 - 5 * r0)/(2 + r0)
# et [et>=1.0] = 1

fig, (ax1, ax3) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]}, sharex=True, figsize = (8.2, 6))

ax1.set_ylabel('anisotropy', color = 'g')  # we already handled the x-label with ax1
ax1.set_ylim(-0.285714, 0.40)
ax1.plot(beta_deg[0:10], portrait_r0[0:10], 'go-')
ax1.plot(beta_deg[0:10], r0[0:10], 'g--')
ax1.tick_params(axis='y', labelcolor='g')
ax1.legend(['portrait r', 'analytical r'], bbox_to_anchor=(0.0, 0.35, 0.5, 0.5))

ax2 = ax1.twinx()  

ax2.set_ylabel('energy transfer efficiency', color='r')
ax2.plot(beta_deg[0:10], funnel_et[0:10], 'ro-')
ax2.plot(beta_deg[0:10], et[0:10], 'r--')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim (0.0, 2.0)
ax2.legend(['funnel et', 'analytical et'], bbox_to_anchor=(0.0, -0.1, 0.5, 0.5)) 


ax3.plot(beta_deg[0:10], residue[0:10],'ko-')
ax3.legend(['residue'])
ax3.set_xlabel('\u03B2 (angle between two dipoles)')
ax3.set_ylim([-0.01, 0.1])

# %%
## 3. plot epsilon - N  for different anglesv(angle12)
## nReplicates = 50
## angle12 = 20

N = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50, 100])
funnel_M = np.array([0.99, 0.56, 0.96, 0.79, 0.86, 0.77, 0.74, 0.61, 0.75, 0.61, 0.42, 0.34, 0.23])
funnel_et = np.array([1.00, 0.66, 0.40, 0.31, 0.30, 0.29, 0.29, 0.28, 0.25, 0.25, 0.24, 0.24, 0.24])
funnel_resi = np.array([0.00, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.009, 0.007, 0.005])

plt.figure()
plt.plot(N, funnel_et, 'ro-')



# %%
## 2. two dipoles - a large system N = 100
## plot angle - epsilon . The angle here is right. It is '+-' 
## nreplicates = 50
## N = 100
## angle_12 = 0 : 180
## et_matrix = np.matrix([[0.0, 1.0],
##                        [0.0, 1.0]])
## boundary of funnel_M < 0.1 

## funnel et
beta = np.linspace(0, 180, 19) # the angle between dipoles in degree
funnel_et = np.array([0,	0.065,	0.243,	0.514,	0.834,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0.828,	0.502,	0.249,	0.068,	0])

# analytical solution et 
beta_r = beta * np.pi / 180
r0 = 0.2 * (3 * np.cos(beta_r) **2 - 1)
analytical_et = (2 - 5 * r0)/(2 + r0)


plt.figure()
plt.plot(beta, funnel_et, 'ro-')
plt.plot(beta, analytical_et, 'ko-')

plt.ylim([0, 2])
plt.xlabel('beta (angle between two dipoles)')
plt.ylabel('et')
plt.legend(['funnel et', 'analytical et'])




# %%
# 1. epsilon - N. The angle here is not right. It should be angle_12 = +-30
# nreplicates = 50
# angle_12 = 30 
# et_matrix = np.matrix([[0.0, 1.0],
#                       [0.0, 1.0]])

x = np.array([1, 2, 4, 8, 16, 32, 64, 128])
y_et = np.array([1.000, 0.546, 0.366, 0.286, 0.265, 0.255, 0.253, 0.252])
 y_M = np.array([0.999, 0.878, 0.815, 0.647, 0.567, 0.359, 0.261, 0.194])

plt.figure(figsize = (17, 4))
plt.subplot(121)
plt.plot(x, y_et, 'ko-')
plt.ylim([0, 1.2])
plt.xlabel('N (number of systems)')
plt.ylabel('funnel et')

plt.subplot(122)
plt.plot(x, y_M, 'ko-')
plt.ylim([0, 1.2])
plt.xlabel('N (number of systems)')
plt.ylabel('funnel M')


# %% ensemble isotropic level. 2D portrait in 3D. explain the relation between r and epsilon
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

model = P.modelfine_output 
Fet = P.Fetfine_output 
Fnoet = P.Fnoetfine_output 
I = np.sum(P.I_ex_em)


exafine = np.linspace( 0, np.pi, 181 )
emafine = np.linspace( 0, np.pi, 181 )
EXfine, EMfine = np.meshgrid(exafine, emafine)

## 3D
fig1 = plt.figure()
fig1.colorbar
ax1 = fig1.add_subplot(111, projection='3d')
surf1 = ax1.plot_surface(EXfine*180/np.pi, EMfine*180/np.pi, I*model/np.max(I*model), cmap=cm.viridis)
surf1.set_clim(0, 1) 
surf2 = ax1.plot_surface(EXfine*180/np.pi, EMfine*180/np.pi, 0.3*I*Fet/np.max(I*model), cmap=cm.viridis)
surf2.set_clim(0, 1) 
surf3 = ax1.plot_surface(EXfine*180/np.pi, EMfine*180/np.pi, 0.7*I*Fnoet/np.max(I*model), cmap=cm.viridis)
surf2.set_clim(0, 1) 

fig1.colorbar(surf1)


## 2D
fig, (ax1, ax2, ax3) = plt.subplots(figsize = (17, 4), ncols = 3)
h_model = ax1.imshow(I * model)
vmax = 375.5551077660677        
h_model.set_clim(0, vmax)        
ax1.invert_yaxis()       
ax1.set_title('model')       
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="5%", pad=0.05)
fig.colorbar(h_model, cax = cax1, ax = ax1)
                
h_Fet = ax2.imshow(0.4 * I * Fet)
h_Fet.set_clim(0, vmax)    
ax2.invert_yaxis()       
ax2.set_title('Fet')       
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="5%", pad=0.05)
fig.colorbar(h_Fet, cax = cax2, ax = ax2)
        
h_Fnoet = ax3.imshow(0.6 * I * Fnoet)
h_Fnoet.set_clim(0, vmax)    
ax3.invert_yaxis()       
ax3.set_title('Fnoet')       
divider3 = make_axes_locatable(ax3)
cax3 = divider3.append_axes("right", size="5%", pad=0.05)
fig.colorbar(h_Fnoet, cax = cax3, ax = ax3)

















    