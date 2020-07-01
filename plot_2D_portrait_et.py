# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:38:33 2020

@author: sjz
"""


import numpy as np
import matplotlib.pyplot as plt
import collection_of_functions as cf
#from mpldatacursor import datacursor 

# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.
et_matrix = np.matrix([[0, 1],
                      [0, 1]])

# singele dipole orientation, 
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 
theta = np.array([0, 90]) # input polar angles in degree
dip_ori = cf.get_dip_ori_2d (theta)

# excitation and emission angles
ex_angles  = np.linspace( 0, 180, 181 )
em_angles  = np.linspace( 0, 180, 181 )

# excitation electric field
E_excitation = cf.get_ex_electric_field()

# Polarizer
E_polarizer = cf.get_em_polarizer()

# excite the sample using linearly polarized light at different angles
E_absorption = np.dot(E_excitation, dip_ori)
I_absorption = E_absorption ** 2
# plt.plot(np.linspace(0,np.pi,181),E_absorption)
# plt.plot(np.linspace(0,np.pi,181),I_absorption)

# Detect the emission polarization by a polarizor
E_emission = np.dot(E_polarizer, dip_ori)
I_emission = E_emission ** 2
# plt.plot(np.linspace(0,np.pi,181),E_emission)
# plt.plot(np.linspace(0,np.pi,181),I_emission)

# change I_absorption and I_emission from array to matrix so that we can have dot product.
I_absorption = np.matrix(I_absorption)
I_emission = np.matrix(I_emission) 

# I_ex_em = I_ex * et_matrix * I_em.T
I_absorption_after_et = np.dot(I_absorption, et_matrix) 
I_ex_em = np.dot(I_absorption_after_et, I_emission.T)
I_ex_em = I_ex_em.T

# plot 2D portrait and ex em curve
plt.figure()
ax1 = plt.subplot(121)
plt.xlabel('ex')
plt.ylabel('em')
plt.gca().invert_yaxis()
plt.draw()

ax2 = plt.subplot(122)
ax2.plot (ex_angles, np.sum(I_ex_em, 0).T, 'b', em_angles, np.sum(I_ex_em,1), 'r')
plt.xlabel('angles')
plt.ylabel('intensity')
ax2.axis('square')

