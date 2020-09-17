# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 10:34:59 2020

@author: sjz
"""

## collection of data

import numpy as np
import matplotlib.pyplot as plt
# %%
# 5. 'three dipoles' - a large system consisting of 1000 molecules
# beta - Mex - et- anisotropy 
#bl = np.array([0, 1, 1])
#et_matrix = np.matrix([[1.0, 0.0, 0.0],
#                       [1.0, 0.0, 0.0],
#                       [1.0, 0.0, 0.0]])
#N_system = np.array([1000])

beta = np.array([0, 10, 20, 30, 40, 45])
Mex = np.array([1.00, 	0.93,	0.77,	0.50,	0.17,	0.00])
portrait_r0 = np.array([0.386,	0.351,	0.273,	0.148,	0.069,	0.009])
funnel_et = np.array([0.000,	0.060,	0.234,	0.501,	0.827,	1.000])

plt.figure()
plt.plot(beta, funnel_et, 'ro-')
plt.plot(beta, portrait_r0, 'yo-')

plt.ylim([-0.5, 1.2])
plt.xlabel('beta (angle between the side and center dipoles)')
plt.legend(['funnel et', 'r0'])

plt.figure()
plt.plot(Mex, funnel_et, 'ro-')
plt.plot(Mex, portrait_r0, 'yo-')

plt.ylim([-0.5, 1.2])
plt.xlabel('Mex')
plt.legend(['funnel et', 'r0'])



# %%
# 4.'two dipoles' - a large system consisting of 1000 molecules
# beta - et- anisotropy 
# nReplicates = 1
# bl = np.array([1, 0])
# et_matrix = np.matrix([[0.0, 1.0],
#                       [0.0, 1.0]])
# N_system = np.array([1000])

beta = np.linspace(0, 180, 19)
portrait_r0 = np.array([0.381,	0.352,	0.304,	0.175,	0.078,	-0.048,	-0.168,	-0.235,	-0.262,	-0.276,	-0.272,	-0.226,	-0.151,	-0.071,	0.080,	0.194,	0.265, 0.364, 0.406])
funnel_et = np.array([0.000,	0.061,	0.234,	0.499,	0.826,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	1.000,	0.827,	0.500,	0.234, 0.06, 0.00])

plt.figure()
plt.plot(beta, funnel_et, 'ro-')
plt.plot(beta, portrait_r0, 'yo-')

plt.ylim([-0.5, 2])
plt.xlabel('beta (angle between two dipoles)')
plt.legend(['funnel et', 'portrait r0'])

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
    