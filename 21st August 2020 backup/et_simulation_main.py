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


# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 

# small number of dipolse (mainly for checking)
# set dipole orientation
# theta = np.array([0, 60])

# set steady state ET matrix
# et_matrix = np.matrix([[0.5, 0.5],
#                       [0, 1]])


# large number of dipoles

# set dipole orientation
theta = np.linspace(0, 180, 1000, endpoint = False)
# theta = np.array(random.sample(range(0, 180), 100))

# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.

# noET
#et_matrix_size = np.size(theta)
#et_matrix = np.eye(et_matrix_size, dtype = int) 

# ET: one or many funnels
et_matrix_size = np.size(theta)
et_matrix = np.matrix([[0.001 for x in range(et_matrix_size)] for y in range(et_matrix_size)] )
#et_matrix[:,0] = 0.4 # emitter1 
#et_matrix[:,30] = 0.3 # emitter2 
#et_matrix[:,60] = 0.3 # emitter3

# ET: the case that SFA+3 does not work 
#et_matrix_size = np.size(theta)
#et_matrix = np.flip(np.eye(et_matrix_size, dtype = int), 1)



# create instance P by class Polim
P = Polim(theta, et_matrix)

# compute and plot 2D portrait
P.compute_2D_portrait()
P.plot_2D_portrait()

#  fit by SFA+3 model and plot the results
P.compute_SFA3()
P.plot_SFA3()

# reconstruct et and noet 2D portrait  
P.reconstruct_Ftot_Fet_Fnoet()


