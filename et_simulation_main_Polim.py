# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:34:56 2020

@author: Juanzi
"""

import numpy as np
from Polim import Polim
import addcopyfighandler

# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 
theta = np.array([0, 60])

# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.
et_matrix = np.matrix([[1, 0],
                       [0, 1]])

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

  
