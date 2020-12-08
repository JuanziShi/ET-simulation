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
plt.close('all')
# %%
# small number of dipoles

# input dipole orientation (polar angles) in degree
# dipole is placed on yz plane, light come from x axis
# (x, y, z), y - 90 degree, z - 180 degree 

# small number of dipolse (mainly for checking)
# set dipole orientation
theta = np.array([0, 30, 60, 90])

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
bl = np.array([1, 1, 1, 1])
bl = (bl == 1)
assert np.size(bl) == np.size(theta), 'bl array is wrong'


# set steady state ET matrix
# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.
et_matrix = np.matrix([[1.0, 0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 1.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0]
                       ])
assert np.sum(et_matrix) == np.size(theta), 'et_matrix is wrong'                

# plt.close('all')
# create instance P by class Polim
P = Polim(theta, bl, et_matrix)

# compute2D portrait
P.compute_2D_portrait()
P.compute_M_phase_from_original_2D_portrait()

# compute anisotropy for large systems (solution)
# P.compute_anisotropy_for_solution()

#  fit by SFA+3 model the results
P.compute_SFA3()

# reconstruct et and noet 2D portrait  
P.reconstruct_Ftot_Fet_Fnoet()

# plot original 2D portrait
P.plot_2D_portrait()

# plot SFA3 fitting results
P.plot_SFA3()

# compare the funnel with dipoles
# P.quick_check_funnel_and_dipoles()


# P.compute_SFA3_unsymmetric()

# # reconstruct et and noet 2D portrait  
# P.reconstruct_Ftot_Fet_Fnoet_unsymmetric()

# # plot original 2D portrait
# P.plot_2D_portrait()

# # plot SFA3 fitting results
# P.plot_SFA3_unsymmetric()

# # compare the funnel with dipoles
# # P.quick_check_funnel_and_dipoles()

# %%
# large number of dipoles

# set dipole orientation
theta = np.linspace(90, 180, 1000, endpoint = False)
# theta = np.array(random.sample(range(0, 180), 100))

# select dipoles to excite by generate a logic matrix. 1 means excite, 0 means not excite.
bl = np.ones(np.size(theta))
bl = (bl == 1)
assert np.size(bl) == np.size(theta), 'bl array is wrong'


# set steady state ET matrix 
# Note! In the paper and Rafael's program, the np.sum(et.matrix,1) = 1 always.

# # noET
# et_matrix_size = np.size(theta)
# et_matrix = np.eye(et_matrix_size, dtype = int) 

# ET: one or many funnels
et_matrix_size = np.size(theta)
et_matrix = np.matrix([[0.00 for x in range(et_matrix_size)] for y in range(et_matrix_size)] )
# emitter1 
et_matrix[:, 999] = 1.0
# emitter2 
#et_matrix[:,200] = 0.6 

# et_matrix[0, 0] = 1.0
# et_matrix[0, 200] = 0.0
# et_matrix[200, 200] = 1.0
# et_matrix[200, 0] = 0.0

# emitter3
#et_matrix[:,400] = 0.3 

# ET: the case that SFA+3 does not work 
#et_matrix_size = np.size(theta)
#et_matrix = np.flip(np.eye(et_matrix_size, dtype = int), 1)

assert np.sum(et_matrix) == np.size(theta), 'et_matrix is wrong' 


plt.close('all')
# create instance P by class Polim
P = Polim(theta, bl, et_matrix)

# compute2D portrait
P.compute_2D_portrait()
P.compute_M_phase_from_original_2D_portrait()

# compute anisotropy for large systems (solution)
P.compute_anisotropy_for_solution()

#  fit by SFA+3 model the results
P.compute_SFA3()

# reconstruct et and noet 2D portrait  
P.reconstruct_Ftot_Fet_Fnoet()

# plot original 2D portrait
P.plot_2D_portrait()

# plot SFA3 fitting results
P.plot_SFA3()

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

# r0 - ex
model = P.modelfine_output
Fet = P.Fetfine_output
Fnoet = P.Fnoetfine_output

model_Ipara = model.diagonal() 
model_Iperp_1 = model[90:181, 0:91].diagonal()
model_Iperp_2 = model[0:90, 90:180].diagonal() 
model_Iperp = np.concatenate((model_Iperp_1, model_Iperp_2))

model_r0 = (model_Ipara - model_Iperp) / (model_Ipara + 2 * model_Iperp)

Fet_Ipara = Fet.diagonal() 
Fet_Iperp_1 = Fet[90:181, 0:91].diagonal()
Fet_Iperp_2 = Fet[0:90, 90:180].diagonal() 
Fet_Iperp = np.concatenate((Fet_Iperp_1, Fet_Iperp_2))

Fet_r0 = (Fet_Ipara - Fet_Iperp) / (Fet_Ipara + 2 * Fet_Iperp)

Fnoet_Ipara = Fnoet.diagonal() 
Fnoet_Iperp_1 = Fnoet[90:181, 0:91].diagonal()
Fnoet_Iperp_2 = Fnoet[0:90, 90:180].diagonal() 
Fnoet_Iperp = np.concatenate((Fnoet_Iperp_1, Fnoet_Iperp_2))

Fnoet_r0 = (Fnoet_Ipara - Fnoet_Iperp) / (Fnoet_Ipara + 2 * Fnoet_Iperp)

x = np.linspace(0, 180, 181)

plt.figure()
plt.plot(x, model_r0)
plt.plot(x, Fet_r0)
plt.plot(x, Fnoet_r0)

plt.xlabel('ex angles')
plt.ylabel('anisotropy')
plt.legend(['model', 'Fet', 'Fnoet'])


plt.figure()
plt.imshow(model)
(model[30,30]-model[30+90,30])/(model[30,30]+2*model[30+90,30])


# Iex, Iem from raw, model, et, noet portrait
model = P.modelfine_output
Fet = P.Fetfine_output
Fnoet = P.Fnoetfine_output
raw_portrait = P.I_ex_em

x = np.linspace(0, 180, 181)

model_I_ex = np.sum(model, axis = 0)
model_I_em = np.sum(model, axis = 1)

Fet_I_ex = np.sum(Fet, axis = 0)
Fet_I_em = np.sum(Fet, axis = 1)

Fnoet_I_ex = np.sum(Fnoet, axis = 0)
Fnoet_I_em = np.sum(Fnoet, axis = 1)

raw_portrait_I_ex = np.sum(np.array(raw_portrait), axis = 0)
raw_portrait_I_em = np.sum(np.array(raw_portrait), axis = 1)

plt.figure()
plt.plot(x, model_I_ex*np.sum(raw_portrait))
plt.plot(x, Fet_I_ex*np.sum(raw_portrait))
plt.plot(x, Fnoet_I_ex*np.sum(raw_portrait))
plt.plot(x, raw_portrait_I_ex)
plt.legend(['model', 'Fet', 'Fnoet', 'raw portrait'])

plt.figure()
plt.plot(x, model_I_em*np.sum(raw_portrait))
plt.plot(x, Fet_I_em*np.sum(raw_portrait))
plt.plot(x, Fnoet_I_em*np.sum(raw_portrait))
plt.plot(x, raw_portrait_I_em)
plt.legend(['model', 'Fet', 'Fnoet', 'raw portrait'])

error = raw_portrait/(model*np.sum(raw_portrait))
plt.figure()
plt.imshow(error)
plt.gca().invert_yaxis()
plt.colorbar()




















