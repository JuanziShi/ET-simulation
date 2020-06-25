# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:38:33 2020

@author: sjz
"""

import collection_of_functions as cf
import numpy as np
import matplotlib.pyplot as plt

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

# ex * em = 2D polarization image
I_absorption = np.matrix(I_absorption)
I_emission = np.matrix(I_emission).T 

I = np.dot(I_absorption, I_emission)

# plot 2D portrait
plt.figure()
ax = plt.imshow(I)
plt.gca().invert_yaxis()
plt.draw()


















 