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

# small number of dipolse (mainly for checking)
# set dipole orientation
theta = np.array([0, 30])

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
bl = np.array([1, 0])
bl = (bl == 1)
assert np.size(bl) == np.size(theta), 'bl array is wrong'


# set steady state ET matrix
et_matrix = np.matrix([[0.0, 1.0],
                       [0.0, 1.0],
                       ])
assert np.sum(et_matrix) == np.size(theta), 'et_matrix is wrong'                


# large number of dipoles

# set dipole orientation
# theta = np.linspace(0, 180, 1000, endpoint = False)
# theta = np.array(random.sample(range(0, 180), 100))

# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.

# noET
#et_matrix_size = np.size(theta)
#et_matrix = np.eye(et_matrix_size, dtype = int) 

# ET: one or many funnels
# et_matrix_size = np.size(theta)
# et_matrix = np.matrix([[0.001 for x in range(et_matrix_size)] for y in range(et_matrix_size)] )
#et_matrix[:,0] = 0.4 # emitter1 
#et_matrix[:,30] = 0.3 # emitter2 
#et_matrix[:,60] = 0.3 # emitter3

# ET: the case that SFA+3 does not work 
#et_matrix_size = np.size(theta)
#et_matrix = np.flip(np.eye(et_matrix_size, dtype = int), 1)


plt.close('all')
# create instance P by class Polim
P = Polim(theta, bl, et_matrix)

# compute and plot 2D portrait
P.compute_2D_portrait()
P.compute_M_phase_from_original_2D_portrait()
P.plot_2D_portrait()


#  fit by SFA+3 model and plot the results
P.compute_SFA3()
P.plot_SFA3()

# reconstruct et and noet 2D portrait  
P.reconstruct_Ftot_Fet_Fnoet()

# compare the funnel with dipoles
P.quick_check_funnel_and_dipoles()





# test= np.array([[0,   1,   2,   3],
#                [5,   15,   20,   32],
#                [10,  11,   21,   13]])

# bl = np.array([1, 0, 1, 1])
# bl = (bl == 1)

# test_c = np.zeros(np.shape(test))
# test_c[:,bl] = test[:,bl]

# print (test_c)























