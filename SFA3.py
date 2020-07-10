# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 18:15:54 2020

@author: Juanzi
"""

def SFA3(M_ex, phase_ex, I_ex_em):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from collection_of_functions import SFA_full_error, SFA_full_func
    import scipy.optimize as so

    # fit by SFA+3 model
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
    column_index = list(range(0,180,30)) # coordinate - angels - intensity. 6 angles for excitation
    row_index = list(range(0,180,45)) # coordinate - angels - intensity. 4 angles for emission

    Ftot = np.empty((0, 6))

    for i in row_index:
        Ftot = np.append(Ftot, I_ex_em[i, column_index]) 
        # print(Ftot)
    
    # normalization. It is according to movie.py, line 1138
    # Note, after normalization, np.sum(Ftotnormed = 1)
    Ftotnormed = Ftot/np.sum(Ftot)

    funargs = (EX, EM, M_ex, phase_ex, Ftotnormed)

    fac = 1e4 
    pg = 1e-9 
    epsi = 1e-11

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
    
    
    # plot fitting results: model, Fet, Fnoet. 
    # This is a good way to check fitting property
    samsum = np.sum(Ftot)
    Fnoet = SFA_full_func( [md_fu,th_fu,gr,0], EX, EM, M_ex, phase_ex )
    Fet   = SFA_full_func( [md_fu,th_fu,gr,1], EX, EM, M_ex, phase_ex )
    model = SFA_full_func( [md_fu,th_fu,gr,et], EX, EM, M_ex, phase_ex)

    plt.figure(figsize= [9, 4])
    plt.interactive(True)
    plt.cla()
    plt.plot( samsum*Fet, 'r-', alpha=.4 )
    plt.plot( samsum*Fnoet, 'b-', alpha=.4 )
    plt.plot( samsum*model, 'g-', alpha=.4 )
    plt.plot( samsum*Ftotnormed, '--', color='gray' )
    plt.legend(['Fet', 'Fnoet', 'model', 'Ftotnormed'])
    plt.title( 'md_fu=%f th_fu=%f gr=%f et=%f resi=%f' % (md_fu,th_fu,gr,et,resi))
    # plt.plot(samsum*(et*Fet + (1-et)*Fnoet)) # equal to model
    
    return fitresult



