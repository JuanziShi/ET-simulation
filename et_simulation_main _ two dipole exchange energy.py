# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 17:59:46 2020

@author: Juanzi
"""
import numpy as np
import matplotlib.pyplot as plt
import addcopyfighandler
from plot_2D_portrait import plot_2D_portrait
from SFA3 import SFA3

results = np.empty([19, 2])
n = 0

for x in np.linspace(0, 190, 19, endpoint = False):
# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 
    theta = np.array([0, 60])

# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.
    et_matrix = np.matrix([[0, 1],
                           [0, 1]])

# plot 2D portrait
    I0, M_ex, phase_ex, M_em, phase_em, I_ex_em = plot_2D_portrait(theta, et_matrix)

#  fit by SFA+3 model and plot the results
    fitresult = SFA3(M_ex, phase_ex, I_ex_em)
    
    plt.close('all')
    

    results[n][0] = x
    results[n][1] = fitresult[1]
    n = n + 1
    print(n)
    
    #print(x)
    #print(fitresult[1])

plt.figure()    
plt.plot(results[:, 0], results[:, 1], 'b')
plt.xlabel('Angle between two dipoles', fontsize = 14)
plt.ylabel('Residue', fontsize = 14)

