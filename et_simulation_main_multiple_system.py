# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:53:26 2020

@author: Juanzi
"""

import numpy as np
import matplotlib.pyplot as plt
import addcopyfighandler
import random

from Polim import Polim

# %%
# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 

# set dipole orientation
theta_1 = np.linspace(0, 180, 1000, endpoint = False)
theta_2 = np.linspace(0, 180, 1000, endpoint = False)
theta_3 = np.linspace(0, 180, 1000, endpoint = False)
# theta = np.array(random.sample(range(0, 180), 100))

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
bl = np.ones(np.size(theta_1))
bl = (bl == 1)
assert np.size(bl) == np.size(theta_1), 'bl array is wrong'


# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.

et_matrix_size = np.size(theta_2)

# noET
et_matrix_1 = np.eye(et_matrix_size, dtype = int) 
assert np.sum(et_matrix_1) == np.size(theta_1), 'et_matrix is wrong' 

# ET: one or many funnels
et_matrix_2 = np.eye(et_matrix_size, dtype = int) / 1.25
et_matrix_2[:,0] = 0.2
et_matrix_2[0,0] = 1
assert np.sum(et_matrix_2) == np.size(theta_2), 'et_matrix is wrong' 

et_matrix_3 = np.matrix([[0.00 for x in range(et_matrix_size)] for y in range(et_matrix_size)] )
et_matrix_3[:,200] = 0.8 
et_matrix_3[:,400] = 0.2
assert np.sum(et_matrix_3) == np.size(theta_3), 'et_matrix is wrong' 




# %%
# # create instance P_1 by class Polim
P_1 = Polim(theta_1, bl, et_matrix_1)
P_1.compute_2D_portrait()
P_1.compute_M_phase_from_original_2D_portrait()
P_1.compute_SFA3()
P_1.plot_SFA3()
P_1.reconstruct_Ftot_Fet_Fnoet()
P_1.plot_2D_portrait()

# create instance P_2 by class Polim
P_2 = Polim(theta_2, bl, et_matrix_2)
P_2.compute_2D_portrait()
P_2.compute_M_phase_from_original_2D_portrait()
P_2.compute_SFA3()
P_2.plot_SFA3() 
P_2.reconstruct_Ftot_Fet_Fnoet()
P_2.plot_2D_portrait()

# create instance P_3 by class Polim
P_3 = Polim(theta_3, bl, et_matrix_3)
P_3.compute_2D_portrait()
P_3.compute_M_phase_from_original_2D_portrait()
P_3.compute_SFA3()
P_3.plot_SFA3() 
P_3.reconstruct_Ftot_Fet_Fnoet()
P_3.plot_2D_portrait()

#plt.close('all')

# create P_ms by sum I_ex_em from P_1, P_2, P_3 
P_ms = Polim(theta_1, bl, et_matrix_1)
ms_I_ex_em = P_1.I_ex_em + P_2.I_ex_em + P_3.I_ex_em
# input 2D portrait of multiple system (ms)
P_ms.I_ex_em = ms_I_ex_em

P_ms.compute_M_phase_from_original_2D_portrait()
P_ms.compute_SFA3()
P_ms.plot_SFA3()  
P_ms.reconstruct_Ftot_Fet_Fnoet()
P_ms.plot_2D_portrait()


















