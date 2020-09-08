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

# Three dipoles
# because we generate dipole randomly, so the calculation needs to be run for several times. 
# The resutls can be different and save in funnel_***.
nReplicates = 50

# the angle between first dipole and second dipole (in degree)
angle_12 = 30.0

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
# the first one is the center dipole, second and third dipoles are symmetric
bl = np.array([0, 1, 1])
bl = (bl == 1)
assert np.size(bl) == 3 , 'bl array is wrong'

# set steady state ET matrix
et_matrix = np.matrix([[1.0, 0.0, 0.0],
                       [1.0, 0.0, 0.0],
                       [1.0, 0.0, 0.0]])
assert np.sum(et_matrix) == 3 , 'et_matrix is wrong'

N_system = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50, 100])
# N_system = np.array([1])

# store the fitting results in following column arrays
funnel_M = np.zeros((nReplicates, np.size(N_system)))
funnel_phase = np.zeros((nReplicates, np.size(N_system)))
funnel_et = np.zeros((nReplicates, np.size(N_system)))
funnel_resi = np.zeros((nReplicates, np.size(N_system)))


# N is the number of systems. in each eystem there are two dipoles oriented at dip1_ori_deg and dip1_ori_deg + angle12
# N = 1, there are two angles in the theta
n_column = 0
for N in N_system:

    #plt.close('all')

    for r in range(0, nReplicates):

        dip1_ori_deg = [] 
        for i in range(0, N):
            t1 = random.randint(0, 180)
            # the orientation of center dipole
            dip1_ori_deg.append(t1)

        # the orientation of the second dipole (= first dipole + angle12)
        dip_ori_deg_pos = [dip2_ori_deg + angle_12  for dip2_ori_deg in dip1_ori_deg]
        dip_ori_deg_neg = [dip2_ori_deg - angle_12  for dip2_ori_deg in dip1_ori_deg]
    
#        print (dip1_ori_deg)
#        print (dip_ori_deg_pos)
#        print (dip_ori_deg_neg)


        ms_I_ex_em = np.zeros((181, 181))

        for n in range(0, N):
    
            # input dipole orientation (polar angles) in degree
            # dipole is placed on yz plane, light come from x axis
            # (x, y, z), y - 90 degree, z - 180 degree 
            theta = np.array([dip1_ori_deg[n], dip_ori_deg_pos[n], dip_ori_deg_neg[n]])
            # print (theta)                 
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
        funnel_M[r][n_column] = P_ms.fitresult[0][0]
        funnel_phase[r][n_column] = P_ms.fitresult[0][1]
        funnel_et[r][n_column] = P_ms.fitresult[0][3]
        funnel_resi[r][n_column] = P_ms.fitresult[1]
        
        if nReplicates == 1 and np.size(N_system) == 1:  
            plt.close('all')
            P_ms.plot_SFA3()
            P_ms.reconstruct_Ftot_Fet_Fnoet()
            P_ms.plot_2D_portrait()
        
    n_column = n_column + 1
    

   
plt.figure()
plt.plot(N_system, np.mean(funnel_et, axis = 0), 'ro-')
plt.plot(N_system, np.mean(funnel_M, axis = 0), 'ko-')
plt.plot(N_system, np.mean(funnel_resi, axis = 0), 'yo-')


# %% save data in .dat file

data_save = np.vstack( (N_system, \
                        np.mean(funnel_M, axis = 0), \
                        np.mean(funnel_et, axis = 0),\
                        np.mean(funnel_resi, axis = 0),\
                        ))
np.savetxt('beta30-Mex-3dipoles-nReplicates50.dat', data_save)


# %% three dipoles - read data and plot
 
# read data
path = 'C:/Users/sjz/Desktop/ET-simulation-master/ET-simulation/results/plot N-epsilon for different Mex (3 dipoles)/'
data0 = np.loadtxt(path+'beta0-Mex1-3dipoles-nReplicates50.dat')
data10 = np.loadtxt(path+'beta10-Mex0.93-3dipoles-nReplicates50.dat')
data20 = np.loadtxt(path+'beta20-Mex0.77-3dipoles-nReplicates50.dat')
data30 = np.loadtxt(path+'beta30-Mex0.5-3dipoles-nReplicates50.dat')
data40 = np.loadtxt(path+'beta40-Mex0.17-3dipoles-nReplicates50.dat')
data45 = np.loadtxt(path+'beta45-Mex0.0-3dipoles-nReplicates50.dat')

# plot raw data
plt.figure()
plt.plot(data0[0,:], data0[2,:], 'o-')
plt.plot(data10[0,:], data10[2,:], 'o-')
plt.plot(data20[0,:], data20[2,:], 'o-')
plt.plot(data30[0,:], data30[2,:], 'o-')
plt.plot(data40[0,:], data40[2,:], 'o-')
plt.plot(data45[0,:], data45[2,:], 'o-')

plt.xlabel('N (number of systems)')
plt.ylabel('funnel et')
plt.legend(['Mex 1', 'Mex 0.93', 'Mex 0.77', 'Mex 0.5', 'Mex 0.17', 'Mex 0.0'])

# plot normalized data
plt.figure()
plt.plot(data0[0,0:11], data0[2,0:11], 'o-')
plt.plot(data10[0,0:11], (data10[2,0:11]-data10[2, 11])/(data10[2,0]-data10[2, 11]), 'o-')
plt.plot(data20[0,0:11], (data20[2,0:11]-data20[2, 11])/(data20[2,0]-data20[2, 11]), 'o-')
plt.plot(data30[0,0:11], (data30[2,0:11]-data30[2, 11])/(data30[2,0]-data30[2, 11]), 'o-')
plt.plot(data40[0,0:11], (data40[2,0:11]-data40[2, 11])/(data40[2,0]-data40[2, 11]), 'o-')
plt.plot(data45[0,0:11], data45[2,0:11], 'o-')

plt.xlabel('N (number of systems)')
plt.ylabel('funnel et')
plt.legend(['Mex 1', 'Mex 0.93', 'Mex 0.77', 'Mex 0.5', 'Mex 0.17', 'Mex 0.0'])
 
# plot Mex - et
Mex = np.array([1, 0.93, 0.77, 0.5, 0.17, 0.0])
funnel_et = np.array([data0[2][12], data10[2][12], data20[2][12], data30[2][12], \
                     data40[2][12], data45[2][12]])
plt.figure()
plt.plot(Mex, funnel_et, 'ro-')
plt.xlabel('Mex')
plt.ylabel('funnel et')                      


# %%
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




    





