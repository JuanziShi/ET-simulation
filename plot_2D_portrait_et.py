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
theta = np.array([0,30]) # input polar angles in degree
dip_ori = cf.get_dip_ori_2d (theta)

# excitation and emission angles
ex_angles  = np.linspace( 0, 180, 181 )
ex_angles_r = ex_angles * np.pi / 180
em_angles  = np.linspace( 0, 180, 181 )
ex_angles_r = ex_angles * np.pi / 180

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

# compute M_ex, phase_ex(in r), M_em, phase_em(in r), 
I0, M_ex, phase_ex, M_em, phase_em = cf.compute_ex_em_modulation_phase (I_ex_em)

'''
# the way I calculate I0, M_ex, phase_ex, M_em, phase_em is fit with 
# the equation I = I0 * (1 + M_em * np.cos(2 * (em_angles * np.pi / 180 - phase_em * np.pi / 180)))

I_ex = I0 * (1 + M_ex * np.cos(2 * (ex_angles * np.pi / 180 - phase_ex)))
I_em = I0 * (1 + M_em * np.cos(2 * (em_angles * np.pi / 180 - phase_em)))
plt.figure()
plt.plot(ex_angles, I_ex, 'b', em_angles, I_em, 'r')
plt.draw()
'''

# plot 2D portrait and ex em curve
plt.figure()
ax1 = plt.subplot(121)
plt.imshow(I_ex_em)
plt.xlabel('ex')
plt.ylabel('em')
plt.gca().invert_yaxis()
plt.draw()

ax2 = plt.subplot(122)
ax2.plot (ex_angles, np.sum(I_ex_em, 0).T, 'b', em_angles, np.sum(I_ex_em,1), 'r')
plt.xlabel('angles')
plt.ylabel('intensity')
ax2.axis('square')


# fit by SFA+3 model
from collection_of_functions import SFA_full_error, SFA_full_func
import scipy.optimize as so

#  def ETmodel_selective( self, myspots, fac=1e4, pg=1e-9, epsi=1e-11 ):

# these three lines are copied from movie.py, line 142, 143 and 1107
# according to line 138 and 139, 6 and 4 correspond to the experimental ex and em angles.
# The angles should be in radian unit
excitation_angles_grid  = np.linspace(0,np.pi,6, endpoint=False)
emission_angles_grid    = np.linspace(0,np.pi,4, endpoint=False)
EX, EM = np.meshgrid(excitation_angles_grid, emission_angles_grid )

# starting point
a0 = [M_ex, phase_ex, 1, .5]

# boundry
LB = [0.001,    phase_ex - np.pi/2, 0, 0]
UB = [0.999999, phase_ex + np.pi/2, 2 * (1 + M_ex)/(1 - M_ex)*.999, 1]

# I_ex_em 181*181. select data and put in Ftotnormed 4*6  
column_index = list(range(0,180,30)) # 6 angles for excitation
row_index = list(range(0,180,45)) # 4 angles for emission

Ftot = np.empty((0, 6))

for i in row_index:
    Ftot = np.append(Ftot, I_ex_em[i, column_index], axis = 0) 
# print(Ftot)
    
# normalization. It is according to movie.py, line 1138
# Note, after normalization, np.sum(Ftot = 1)
Ftotnormed = Ftot/np.sum(Ftot)
# Ftotnormed = Ftotnormed.reshape((Ftotnormed.size,)).T

funargs = (EX, EM, M_ex, phase_ex, Ftotnormed)

fac=1e4 
pg=1e-9 
epsi=1e-11

fitresult = so.fmin_l_bfgs_b( func=SFA_full_error, \
                             x0=a0, \
                             fprime=None, \
                             args=funargs, \
                             approx_grad=True, \
                             epsilon=epsi, \
                             bounds=list(zip(LB,UB)), \
                             factr=fac, \
                             pgtol=pg )

md_fu = fitresult[0][0]
th_fu = fitresult[0][1]
gr    = fitresult[0][2]
et    = fitresult[0][3]
resi  = fitresult[1]























