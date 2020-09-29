# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 10:34:59 2020

@author: sjz
"""

## collection of data

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})

# %%
# 6. unsymmetric absorption. [0 60 70 90]
# no et, the model does not work well.
# et, the higher the et, the better the model.

M	= np.array([0.9999, 0.9999,	0.9928, 0.9901, 0.9918, 0.9938,	0.9956, 0.9970, 0.9982, 0.9992,	0.9999])
phase = np.array([1.6413, 1.2787, 1.1555, 1.1102,	1.0876, 1.0740, 1.0650, 1.0586,	1.0538, 1.0501, 1.0472])
gr = np.array([3.4697, 3.4749, 3.4712,	3.4740, 3.4768, 3.4797, 3.4825,	3.4854, 3.4881, 3.4911, 1.0453])
et = np.array([0.0001, 0.1076, 0.2005,	0.3001, 0.3998, 0.4996, 0.5995,	0.6994, 0.7995, 0.8997, 1.0000])
resi = np.array([0.0355,	0.0311, 0.0277, 0.0242, 0.0207,	0.0173, 0.0138, 0.0104, 0.0069,	0.0035, 0.0000])

phase_deg = phase * 180 / np.pi

plt.figure()
plt.plot(et, resi, 'ko-')
plt.xlabel('et')
plt.ylabel('resi')



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

r0 = (24.0 / 35.0) * np.cos(beta_r)**2 - (2.0 / 7.0)	
et = (2 - 5 * r0)/(2 + r0)	
et [et>=1.0] = 1	

plt.figure()	plt.figure()
plt.plot(beta, funnel_et, 'ro-')	plt.plot(beta, funnel_et, 'ro-')
plt.plot(beta, et, 'k--')	

plt.legend(['funnel et', 'analytical solution'])	
plt.xlabel('beta (angle between the side and center dipoles)')	
plt.ylabel('et')	


plt.figure()	
plt.plot(beta, portrait_r0, 'yo-')	plt.plot(beta, portrait_r0, 'yo-')
plt.plot(beta, r0, 'k--')	


plt.legend(['r0 calculated from 2D portrait', 'analytical solution'])	plt.ylim([-0.5, 1.2])
plt.xlabel('beta (angle between the side and center dipoles)')	plt.xlabel('beta (angle between the side and center dipoles)')
plt.ylabel('r0')	plt.legend(['funnel et', 'r0'])

plt.figure()	plt.figure()
plt.plot(Mex, funnel_et, 'ro-')



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

# theoritical solution
beta_r = beta_deg * np.pi / 180

#r0 = 0.2 * (3 * np.cos(beta_r) **2 - 1)
r0 = (24.0 / 35.0) * np.cos(beta_r)**2 - (2.0 / 7.0)
et = (2 - 5 * r0)/(2 + r0)
et [et>=1.0] = 1


plt.figure()
plt.plot(beta, funnel_et, 'ro-')
plt.plot(beta, et, 'k--')

plt.legend(['funnel et', 'analytical solution'])
plt.xlabel('beta (angle between two dipoles)')
plt.ylabel('et')

plt.figure()
plt.plot(beta, portrait_r0, 'yo-')
plt.plot(beta, r0, 'k--')

plt.legend(['r0 calculated from 2D portrait', 'analytical solution'])
plt.xlabel('beta (angle between two dipoles)')
plt.ylabel('r0')


plt.figure()
plt.plot(funnel_et[0:9], portrait_r0[0:9], 'ko-')
plt.xlabel('funnel et')
plt.ylabel('portrait r0')



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
    