# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

def get_dip_ori_2d (theta):
    ''' 
    this function is used to generate dipole oriented on yz plane
    x = 0, and y^2 + z^2 = 1 
    dip_ori
    [x1 x2 x3 x4 ...
    y1 y2 y3 y4 ...
    z1 z3 z3 z4 ]...
    '''
    
    # polar angle in radian
    theta = theta*np.pi/180 
    
    #azimuthal angle is always pi/2, so the dipole is placed on yz plane
    phi = np.ones(theta.size)*np.pi/2 
    
    dip_ori = np.zeros((3, theta.size))
    
    dip_ori[0,:] = np.cos(phi)*np.sin(theta) # x 
    dip_ori[1,:] = np.sin(phi)*np.sin(theta) # y
    dip_ori[2,:] = np.cos(theta)             # z
    
    # to remove the numerical noise
    dip_ori[0,:] = dip_ori[0,:] * 0 
    
    return dip_ori
 
    
def get_ex_electric_field():
    '''
    this function is used to generate excitation electric field on yz plane
    x = 0, and y^2 + z^2 = 1 
    ex_ori
    [x1 y1 z1
    x2 y2 z2
    x3 y3 z3
    x4 y4 z4 
    .  .  .]
    '''
    
    ex_angles_r  = np.linspace( 0, np.pi, 181 )
    
    # field vector is rotated on the yz plane. In the array (x, y, z)
    ex_ori = np.zeros((ex_angles_r.size, 3))
    
    # spherical coordinates, r is equal to 1
    # azimuthal angle is always 90 degree, becasue we calculate the projection on yz plane.
    phi = np.ones(ex_angles_r.size)*np.pi/2 
    theta = ex_angles_r
    
    # from spherical coordinates to cartesian coordinate. 
    # equation from Rafael's thesis, page 18, eq 13
    ex_ori[:,0] = np.cos(phi)*np.sin(theta) # x
    ex_ori[:,1] = np.sin(phi)*np.sin(theta) # y
    ex_ori[:,2] = np.cos(theta)             # z
    
    # to remove the numerical noise
    ex_ori[:,0] = ex_ori[:,0] * 0 
    
    # plot the excitation E field 
    # plt.scatter( ex_ori[:,1], ex_ori[:,2])
      
    return ex_ori


def get_em_polarizer():
    '''
    this function is a polarizer on yz plane
    x = 0, and y^2 + z^2 = 1 
    ex_ori
    [x1 y1 z1
    x2 y2 z2
    x3 y3 z3
    x4 y4 z4 
    .  .  .]
    '''
    
    em_angles_r = np.linspace(0, np.pi, 181)
    
    #field vector is rotated on the yz plane. In the array (x, y, z)
    em_ori = np.zeros((em_angles_r.size, 3))
    
    # spherical coordinate, r is equal to 1
    # azimuthal angle is always 90 degree, because we calculate the projection on yz plane
    phi = np.ones(em_angles_r.size)*np.pi/2
    theta = em_angles_r
    
    # from spherical coordinates to cartesian coordinate
    # equation from Rafael's thesis, page 18, eq 13
    em_ori[:,0] = np.cos(phi)*np.sin(theta) # x
    em_ori[:,1] = np.sin(phi)*np.sin(theta) # y
    em_ori[:,2] = np.cos(theta)             # z
    
    # to remove numerical noise
    em_ori[:,0] = em_ori[:,0] * 0 
    
    # plot the excitation E field 
    # plt.scatter( em_ori[:,1], em_ori[:,2])
    
    return em_ori
    

def compute_ex_em_modulation_phase(I_ex_em, theta):
    '''Maybe in the furture the CosineFitter_new is needed.
    Now I calculate modulation depth and phases by the sum of 2D portrait'''
    
    I_ex = np.sum(I_ex_em,0).T
    I_em = np.sum(I_ex_em,1)
    
    # calculate I0
    I0 = (np.amax(I_ex) + np.amin(I_ex))/2
    
    # calculate ex modulation depth and phase
    M_ex = (np.amax(I_ex) - np.amin(I_ex))/(np.amax(I_ex) + np.amin(I_ex))

    
    if M_ex < 1e-6:
        M_ex = 0.0
        phase_ex = 45 * np.pi / 180
    else:
        phase_ex = np.argmax(I_ex) * np.pi / 180
    
    # calculate em modulation depth and phase
    M_em = (np.amax(I_em) - np.amin(I_em))/(np.amax(I_em) + np.amin(I_em))
    if M_em < 1e-3:
        M_em = 0.0
        phase_em = np.mean(theta) * np.pi / 180
    else:
        phase_em = np.argmax(I_em) * np.pi / 180
    
    return I0, M_ex, phase_ex, M_em, phase_em 
    

# symmetric three dipole model
def SFA_full_func( params, ex_angles, em_angles, md_ex, phase_ex ):
    
    md_fu = params[0]
    th_fu = params[1]
    gr    = params[2]
    et    = params[3]
    alpha = params[4]

    EX, EM = ex_angles.flatten(), em_angles.flatten()
    # calculate angle between off-axis dipoles in symmetric model
    if np.isnan(gr): gr=1.0
    alpha = 0.5 * np.arccos( .5*(((gr+2.0)*md_ex)-gr) )

    ph_ii_minus = phase_ex - alpha
    ph_ii_plus  = phase_ex + alpha

    # print EX
    # print EM
    # print np.cos( EX-ph_ii_minus )**2 * np.cos( EM-ph_ii_minus )**2
    # raise SystemExit
    Fnoet  =    np.cos( EX-ph_ii_minus )**2 * np.cos( EM-ph_ii_minus )**2
    Fnoet += gr*np.cos( EX-phase_ex )**2 * np.cos( EM-phase_ex )**2
    Fnoet +=    np.cos( EX-ph_ii_plus )**2 * np.cos( EM-ph_ii_plus )**2
    Fnoet /= (2.0+gr)    # irrelevant, because we sum-normalize below!
    Fnoet /= np.sum(Fnoet)

    Fet   = .25 * (1+md_ex*np.cos(2*(EX-phase_ex))) * (1+md_fu*np.cos(2*(EM-th_fu)))
    Fet  /= np.sum(Fet)
    

    return et*Fet + (1-et)*Fnoet
'''

def SFA_full_func( params, ex_angles, em_angles, md_ex, phase_ex ):
    
    #unsymmetric three dipole model
    
    md_fu = params[0]
    th_fu = params[1]
    gr    = params[2]
    et    = params[3]
    alpha = params[4]
    beta  = params[5]

    EX, EM = ex_angles.flatten(), em_angles.flatten()
    # calculate angle between off-axis dipoles in symmetric model
    if np.isnan(gr): gr=1.0
    
    # alpha = 0.5 * np.arccos( .5*(((gr+2.0)*md_ex)-gr) )

    ph_ii_minus = phase_ex - alpha
    ph_ii_plus  = phase_ex + beta

    # print EX
    # print EM
    # print np.cos( EX-ph_ii_minus )**2 * np.cos( EM-ph_ii_minus )**2
    # raise SystemExit
    Fnoet  =    np.cos( EX-ph_ii_minus )**2 * np.cos( EM-ph_ii_minus )**2
    Fnoet += gr*np.cos( EX-phase_ex )**2 * np.cos( EM-phase_ex )**2
    Fnoet +=    np.cos( EX-ph_ii_plus )**2 * np.cos( EM-ph_ii_plus )**2
    Fnoet /= (2.0+gr)    # irrelevant, because we sum-normalize below!
    Fnoet /= np.sum(Fnoet)

    Fet   = .25 * (1+md_ex*np.cos(2*(EX-phase_ex))) * (1+md_fu*np.cos(2*(EM-th_fu)))
    Fet  /= np.sum(Fet)
    

    return et*Fet + (1-et)*Fnoet
'''

def SFA_full_error( params, ex_angles, em_angles, md_ex, phase_ex, Ftot ):
    diff = Ftot - SFA_full_func( params, ex_angles, em_angles, md_ex, phase_ex )

    # import matplotlib.pyplot as plt
    # plt.interactive(True)
    # plt.cla()
    # plt.plot( Ftot, 'b' )
    #plt.plot( SFA_full_func( params, ex_angles, em_angles, md_ex, phase_ex ), 'g' )
    # raise SystemExit

    return np.sqrt(np.sum( diff**2 ))
    
    


    



