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
theta = np.array([0, 60, 120])

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
bl = np.array([1, 1, 1])
bl = (bl == 1)
assert np.size(bl) == np.size(theta), 'bl array is wrong'


# set steady state ET matrix
et_matrix = np.matrix([[1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0]])
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


# plt.close('all')
# create instance P by class Polim
P = Polim(theta, bl, et_matrix)

# compute and plot 2D portrait
P.compute_2D_portrait()
P.compute_M_phase_from_original_2D_portrait()
P.plot_2D_portrait()

# compute anisotropy for large systems (solution)
P.compute_anisotropy_for_solution()

#  fit by SFA+3 model and plot the results
P.compute_SFA3()
# P.plot_SFA3()

# reconstruct et and noet 2D portrait  
# P.reconstruct_Ftot_Fet_Fnoet()

# compare the funnel with dipoles
# P.quick_check_funnel_and_dipoles()


# %% try to extrat the number of dipoles from 2D portrait

# plot the diagonal of the raw 2D portrait
x = np.linspace(0, 180, 181)
raw_portrait_diag = np.diag(P.I_ex_em)
plt.figure()
plt.plot(x, raw_portrait_diag)
plt.ylim(0.0, np.max(raw_portrait_diag) + 0.5)
np.savetxt('raw_portrait_diag4.dat', raw_portrait_diag)


# FFT of image
im = P.I_ex_em
im = np.flip(im, axis = 0)

# FFT
f = np.fft.fft2(im)
# concentrate all high frequency on the center
fshift = np.fft.fftshift(f)

magnitude_spectrum = 20 * np.log(np.abs(fshift))
magnitude_spectrum = np.asarray(magnitude_spectrum, dtype = np.uint16)

im_and_magnitude = np.concatenate((im/np.max(im)*256, magnitude_spectrum), axis = 1)

plt.figure()
plt.imshow(im_and_magnitude)
plt.axis('off')




















