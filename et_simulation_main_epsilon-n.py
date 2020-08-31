# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:34:56 2020

@author: Juanzi
"""

import numpy as np
import matplotlib.pyplot as plt
import addcopyfighandler
import random

from Polim import Polim

plt.rcParams.update({'font.size': 12})
# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 

## small number of dipolse (mainly for checking)
## set dipole orientation in degree
#theta = np.array([0, 60, 100, 160, 80, 20])
#
## set steady state ET matrix
#et_matrix = np.matrix([
#                       [0.8, 0.2, 0.0, 0.0, 0.0, 0.0],
#                       [0.2, 0.8, 0.0, 0.0, 0.0, 0.0],
#                       [0.0, 0.0, 0.8, 0.2, 0.0, 0.0],
#                       [0.0, 0.0, 0.2, 0.8, 0.0, 0.0],
#                       [0.0, 0.0, 0.0, 0.0, 0.8, 0.2],
#                       [0.0, 0.0, 0.0, 0.0, 0.2, 0.8]
#                       ])
#assert np.sum(et_matrix) == np.size(theta), 'et_matrix is wrong'


N = 1 # the number of dipoles 
angle_12 = 60 # the angle between first dipole and second dipole (in degree)

dip1_ori_deg = [] 
for i in range(0,N):
    t1 = random.randint(0, 120)
    # the orientation of first dipole
    dip1_ori_deg.append(t1)

# the orientation of the second dipole (= first dipole + angle12)
dip2_ori_deg = [dip2_ori_deg + angle_12  for dip2_ori_deg in dip1_ori_deg]

#print (dip1_ori_deg) 
#print (dip2_ori_deg) 

ms_I_ex_em = np.zeros((181, 181))

for n in range(0, N):
    
# small number of dipolse (mainly for checking)
# set dipole orientation in degree
    theta = np.array([dip1_ori_deg[n], dip2_ori_deg[n]])

# set steady state ET matrix
    et_matrix = np.matrix([[0.2, 0.8],
                       [0.8, 0.2]])
    assert np.sum(et_matrix) == np.size(theta), 'et_matrix is wrong'
                       
# plt.close('all')
# create instance P by class Polim
    P = Polim(theta, et_matrix)

# compute and plot 2D portrait
    P.compute_2D_portrait()
    P.compute_M_phase_from_original_2D_portrait()
    #P.plot_2D_portrait()


#  fit by SFA+3 model and plot the results
    P.compute_SFA3()
    #P.plot_SFA3()

# reconstruct et and noet 2D portrait  
    #P.reconstruct_Ftot_Fet_Fnoet()

# compare the funnel with dipoles
    # P.quick_check_funnel_and_dipoles()

    ms_I_ex_em = ms_I_ex_em + P.I_ex_em
    

plt.close('all')
# multiple system
P_ms = Polim(theta, et_matrix)
# input 2D portrait of multiple system (ms)
# normalized I_ex_em
P_ms.I_ex_em = ms_I_ex_em/N 
# plot 2D portrait
P_ms.plot_2D_portrait()
P_ms.compute_M_phase_from_original_2D_portrait()
#  fit by SFA+3 model and plot the results
P_ms.compute_SFA3()
P_ms.plot_SFA3()
# reconstruct et and noet 2D portrait  
P_ms.reconstruct_Ftot_Fet_Fnoet()

