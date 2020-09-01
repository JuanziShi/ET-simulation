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





# because we generate dipole randomly, so the calculation needs to be run for several times. 
# The resutls can be different and save in funnel_***.
nReplicates = 50

# store the fitting results in following column arrays
funnel_M = np.zeros((nReplicates, 1))
funnel_phase = np.zeros((nReplicates, 1))
funnel_et = np.zeros((nReplicates, 1))
funnel_resi = np.zeros((nReplicates, 1))


for r in range(0, nReplicates):

    # the number of systems. in each eystem there are two dipoles oriented at dip1_ori_deg and dip1_ori_deg + angle12
    N = 32 
    # the angle between first dipole and second dipole (in degree)
    angle_12 = 40 

    dip1_ori_deg = [] 
    for i in range(0,N):
        t1 = random.randint(0, 180)
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
        et_matrix = np.matrix([[0.0, 1.0],
                               [0.0, 1.0]])
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
    

    # plt.close('all')
    # multiple system
    P_ms = Polim(theta, et_matrix)
    # input 2D portrait of multiple system (ms)
    # normalized I_ex_em
    P_ms.I_ex_em = ms_I_ex_em/N 
    # plot 2D portrait
    # P_ms.plot_2D_portrait()
    P_ms.compute_M_phase_from_original_2D_portrait()
    #  fit by SFA+3 model and plot the results
    P_ms.compute_SFA3()
    #P_ms.plot_SFA3()
    # reconstruct et and noet 2D portrait  
    #P_ms.reconstruct_Ftot_Fet_Fnoet()
    
    funnel_M[r] = P_ms.fitresult[0][0]
    funnel_phase[r] = P_ms.fitresult[0][1]
    funnel_et[r] = P_ms.fitresult[0][3]
    funnel_resi[r] = P_ms.fitresult[1]

plt.close('all')

plt.figure(figsize=(17, 4))

plt.subplot(141)
plt.hist(funnel_M, bins = 20, range = (-0.2,1.2))
plt.title('averaged_funnel_M \n %f ' % (np.mean(funnel_M)))
plt.xlim([-0.2, 1.2])

plt.subplot(142)
plt.hist(funnel_phase * 180/np.pi - angle_12 , bins = 180, range = (-2,182))
plt.title('funnel_phase')

plt.subplot(143)
plt.hist(funnel_et, bins = 20, range = (-0.2,1.2))
plt.title('averaged_funnel_et \n %f' % (np.mean(funnel_et)) )

plt.subplot(144)
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
    

    





