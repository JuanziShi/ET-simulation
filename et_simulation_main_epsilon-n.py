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

# because we generate dipole randomly, so the calculation needs to be run for several times. 
# The resutls can be different and save in funnel_***.
nReplicates = 50


# N is the number of systems. in each eystem there are two dipoles oriented at dip1_ori_deg and dip1_ori_deg + angle12
# N = 1, there are two angles in the theta
N = 20

# the angle between first dipole and second dipole (in degree)
angle_12 = 20.0

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
bl = np.array([1, 0])
bl = (bl == 1)
assert np.size(bl) == 2 , 'bl array is wrong'

# set steady state ET matrix
et_matrix = np.matrix([[0.0, 1.0],
                       [0.0, 1.0]])
assert np.sum(et_matrix) == 2 , 'et_matrix is wrong'


# store the fitting results in following column arrays
funnel_M = np.zeros((nReplicates, 1))
funnel_phase = np.zeros((nReplicates, 1))
funnel_et = np.zeros((nReplicates, 1))
funnel_resi = np.zeros((nReplicates, 1))

plt.close('all')

for r in range(0, nReplicates):

    dip1_ori_deg = [] 
    for i in range(0, N):
        t1 = random.randint(0, 180)
    # the orientation of first dipole
        dip1_ori_deg.append(t1)

    # the orientation of the second dipole (= first dipole + angle12)
    dip2_ori_deg_pos = [dip2_ori_deg + angle_12  for dip2_ori_deg in dip1_ori_deg[0:N/2]]
    dip2_ori_deg_neg = [dip2_ori_deg - angle_12  for dip2_ori_deg in dip1_ori_deg[N/2:N]]
    dip2_ori_deg = np.append(dip2_ori_deg_pos, dip2_ori_deg_neg, axis = 0)
    
    # print (dip1_ori_deg)
    # print (dip2_ori_deg)

    ms_I_ex_em = np.zeros((181, 181))

    for n in range(0, N):
    
        # input dipole orientation (polar angles) in degree
        # dipole is placed on yz plane, light come from x axis
        # (x, y, z), y - 90 degree, z - 180 degree 
        theta = np.array([dip1_ori_deg[n], dip2_ori_deg[n]])
                              
        # create instance P by class Polim
        P = Polim(theta, bl, et_matrix)

        # compute 2D portrait and fit by SFA3
        P.compute_2D_portrait()
        P.compute_M_phase_from_original_2D_portrait()
        P.compute_SFA3()

        ms_I_ex_em = ms_I_ex_em + P.I_ex_em
        
        
    # multiple system
    P_ms = Polim(theta, bl, et_matrix)
    # input 2D portrait of multiple system (ms) to instance P_ms
    # normalized I_ex_em
    P_ms.I_ex_em = ms_I_ex_em/N 
    
    # fit by SFA3
    P_ms.compute_M_phase_from_original_2D_portrait()
    P_ms.compute_SFA3()
    
    # store the data
    funnel_M[r] = P_ms.fitresult[0][0]
    funnel_phase[r] = P_ms.fitresult[0][1]
    funnel_et[r] = P_ms.fitresult[0][3]
    funnel_resi[r] = P_ms.fitresult[1]
    
    if nReplicates == 1:       
        P_ms.plot_SFA3()
        P_ms.reconstruct_Ftot_Fet_Fnoet()
        P_ms.plot_2D_portrait()
        

if nReplicates != 1:
    # plt.close('all')
    # plot statistic results
    plt.figure(figsize=(16, 9))
    plt.subplots_adjust(hspace = 0.4)

    plt.subplot(231)
    plt.scatter(funnel_et, funnel_M)
    plt.xlabel('et')
    plt.ylabel('M')
    plt.xlim([-0.2, 1.2])
    plt.ylim([-0.2, 1.2])

    plt.subplot(232)
    plt.scatter(funnel_et, funnel_resi)
    plt.xlabel('et')
    plt.ylabel('residue')
    plt.xlim([-0.2, 1.2])
    plt.ylim([0.0, 0.1])

    plt.subplot(233)
    plt.scatter(funnel_phase * 180/np.pi, funnel_M)
    plt.xlabel('phase')
    plt.ylabel('M')
    plt.xlim([-2, 182])
    plt.ylim([-0.2, 1.2])

    plt.subplot(245)
    plt.hist(funnel_M, bins = 20, range = (-0.2,1.2))
    plt.title('averaged_funnel_M \n %f ' % (np.mean(funnel_M)))
    plt.xlim([-0.2, 1.2])

    plt.subplot(246)
    plt.hist(funnel_phase * 180/np.pi , bins = 180, range = (-2,182))
    plt.title('funnel_phase')

    plt.subplot(247)
    plt.hist(funnel_et, bins = 20, range = (-0.2,1.2))
    plt.title('averaged_funnel_et \n %f' % (np.mean(funnel_et)) )

    plt.subplot(248)
    plt.hist(funnel_resi)
    plt.title('averaged_funnel_resi \n %f' % (np.mean(funnel_resi)))






# # nreplicates = 50
# # angle_12 = 30 
# # et_matrix = np.matrix([[0.0, 1.0],
# #                       [0.0, 1.0]])
# x = np.array([1, 2, 4, 8, 16, 32, 64, 128])
# y_et = np.array([1.000, 0.546, 0.366, 0.286, 0.265, 0.255, 0.253, 0.252])
# y_M = np.array([0.999, 0.878, 0.815, 0.647, 0.567, 0.359, 0.261, 0.194])

# plt.figure(figsize = (17, 4))
# plt.subplot(121)
# plt.plot(x, y_et, 'ko-')
# plt.ylim([0, 1.2])
# plt.xlabel('N (number of systems)')
# plt.ylabel('funnel et')

# plt.subplot(122)
# plt.plot(x, y_M, 'ko-')
# plt.ylim([0, 1.2])
# plt.xlabel('N (number of systems)')
# plt.ylabel('funnel M')
    

    





