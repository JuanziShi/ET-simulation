# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:38:33 2020

@author: sjz
"""

import collection_of_functions as cf
import numpy as np
import matplotlib.pyplot as plt

# singele dipole orientation
dip_ori = np.array([0, 1, 0])

# multiple dipole orientation
# dip_ori = np.array([[1, 0, 0],[0, 1, 0]]).T

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
 


I_absorption = I_absorption.reshape(1,I_absorption.shape[0])

I = np.dot(I_emission, I_absorption)




t1 = np.array([1, 2, 3])
t2 = t1.reshape(1,t1.shape[0])
d12 = np.determinant(t1,t2)
d21 = np.dot(t2,t1)

t1 = np.matrix([1, 2, 3])
t2 = t1.T
d21 = np.dot(t2,t1)
















 