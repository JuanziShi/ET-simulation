# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:38:33 2020

@author: sjz
"""

import collection_of_functions as cf
import numpy as np
import matplotlib.pyplot as plt

# multiple dipole orientation
# dip_ori = np.array([[1, 0, 0],[0, 1, 0]]).T

# singele dipole orientation
dip_ori = np.array([0, 1, 0])

# excitation electric field
E_ex = cf.get_ex_electric_field()

# Polarizer
E_polarizer = cf.get_em_polarizer

# excite the sample using linearly polarized light at different angles
absorption = np.dot(E_ex, dip_ori)
#plt.plot(np.linspace(0,np.pi,181),absorption)

emission = np.dot(absorption) 