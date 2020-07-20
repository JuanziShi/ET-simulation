# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 17:15:53 2020

@author: Juanzi
"""

def plot_2D_portrait(theta, et_matrix):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import collection_of_functions as cf
                      
    # dipole orientation
    # dipole is placed on yz plane, light come from x axis
    # (x, y, z), y - 90 degree, z - 180 degree 
    # input polar angles in degree (theta)
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
    plt.figure(figsize= [9, 4])

    ax1 = plt.subplot(121)
    plt.imshow(I_ex_em)
    plt.xlabel('ex')
    plt.ylabel('em')
    plt.gca().invert_yaxis()
    plt.draw()
    theta_str = str(theta).strip('[]')
    title_str = 'dipoles orientation =' + theta_str + ' (in degree) '
    plt.title(title_str, fontsize = 14)

    ax2 = plt.subplot(122)
    ax2.plot (ex_angles, np.sum(I_ex_em, 0).T, 'b', em_angles, np.sum(I_ex_em,1), 'r')
    plt.xlabel('angles')
    plt.ylabel('intensity')
    ax2.axis('square')
    
    # compute M_ex, phase_ex(in r), M_em, phase_em(in r), 
    I0, M_ex, phase_ex, M_em, phase_em = cf.compute_ex_em_modulation_phase (I_ex_em)
    
    return I0, M_ex, phase_ex, M_em, phase_em, I_ex_em

    
    

