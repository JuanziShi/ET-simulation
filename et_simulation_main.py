# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 17:59:46 2020

@author: Juanzi
"""
import numpy as np
from plot_2D_portrait import plot_2D_portrait
from SFA3 import SFA3

# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 
theta = np.array([0, 15])

# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.
et_matrix = np.matrix([[0, 1],
                       [1, 0]])

# plot 2D portrait
I0, M_ex, phase_ex, M_em, phase_em, I_ex_em = plot_2D_portrait(theta, et_matrix)

#  fit by SFA+3 model and plot the results
fitresult = SFA3(M_ex, phase_ex, I_ex_em)
