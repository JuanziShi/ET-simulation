# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:18:44 2020

@author: Juanzi
"""

def reconstruct_Ftot_Fet_Fnoet(fitresult, M_ex, phase_ex):
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    md_fu = fitresult[0][0]
    th_fu = fitresult[0][1]
    gr    = fitresult[0][2]
    et    = fitresult[0][3]
    resi  = fitresult[1]
    
    md_ex = M_ex
    phase_ex = phase_ex
    
    exafine = np.linspace( 0, np.pi, 181 )
    emafine = np.linspace( 0, np.pi, 181 )
    EXfine, EMfine = np.meshgrid( exafine, emafine )
    
    if np.isnan(gr): gr=1.0
    alpha = 0.5 * np.arccos( .5*(((gr+2)*md_ex)-gr) )

    ph_ii_minus = phase_ex - alpha
    ph_ii_plus  = phase_ex + alpha
        
    Fnoetfine  =    np.cos( EXfine-ph_ii_minus )**2 * np.cos( EMfine-ph_ii_minus )**2
    Fnoetfine += gr*np.cos( EXfine-phase_ex )**2 * np.cos( EMfine-phase_ex )**2
    Fnoetfine +=    np.cos( EXfine-ph_ii_plus )**2 * np.cos( EMfine-ph_ii_plus )**2
    Fnoetfine /= (2.0+gr)
    Fnoetfine /= np.sum(Fnoetfine)
    
    Fetfine    = .25 * (1 + md_ex * np.cos(2 * (EXfine - phase_ex))) * (1 + md_fu * np.cos(2 * (EMfine - th_fu)))
    Fetfine   /= np.sum(Fetfine)
    
    modelfine  = et * Fetfine + (1 - et) * Fnoetfine
    
    # note: np.sum(modelfine) = 1, np.sum(Fetfine) = 1, np.sum(Fnoetfine) = 1
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 4, 1)
    plt.imshow(modelfine)
    plt.gca().invert_yaxis()
    plt.title('model')
    
    
    plt.subplot(1, 4, 2)
    plt.imshow(Fetfine)
    plt.gca().invert_yaxis()
    plt.title('Fet')

    plt.subplot(1, 4, 3)
    plt.imshow(Fnoetfine)
    plt.gca().invert_yaxis()
    plt.title('Fnoet' )    
    
    plt.subplot(1, 4, 4)
    plt.text(0.1, 0.5, 'et = %0.1f' % et)
    plt.axis('off')
     
    return