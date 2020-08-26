# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 09:43:58 2020

@author: Juanzi
"""

import numpy as np
import matplotlib.pyplot as plt
import collection_of_functions as cf
import scipy.optimize as so
from mpl_toolkits.axes_grid1 import make_axes_locatable


class Polim:
    
           
    def __init__(self, theta, et_matrix):
        
        # input
        self.theta = theta
        self.et_matrix = et_matrix
        
        # excitation and emission angles
        self.ex_angles  = np.linspace( 0, 180, 181 )
        self.ex_angles_r = self.ex_angles * np.pi / 180
        self.em_angles  = np.linspace( 0, 180, 181 )
        self.ex_angles_r = self.ex_angles * np.pi / 180
        
        # compute and plot 2D portrait
        self.dip_ori = None
        self.portrait = None
        self.I_ex_em = None
        
        # fit by SFA3 and plot residue
        self.fitresult = None
        self.Ftot = None
        
        
        return
   
    
    
    def compute_2D_portrait(self):
                      
        # dipole orientation
        # dipole is placed on yz plane, light come from x axis
        # (x, y, z), y - 90 degree, z - 180 degree 
        # input polar angles in degree (theta)
        self.dip_ori = cf.get_dip_ori_2d (self.theta)

        # excitation electric field
        E_excitation = cf.get_ex_electric_field()

        # Polarizer
        E_polarizer = cf.get_em_polarizer()

        # excite the sample using linearly polarized light at different angles
        E_absorption = np.dot(E_excitation, self.dip_ori)
        I_absorption = E_absorption ** 2
        # plt.plot(np.linspace(0,np.pi,181),E_absorption)
        # plt.plot(np.linspace(0,np.pi,181),I_absorption)
        
        # Detect the emission polarization by a polarizor
        E_emission = np.dot(E_polarizer, self.dip_ori)
        I_emission = E_emission ** 2
        # plt.plot(np.linspace(0,np.pi,181),E_emission)
        # plt.plot(np.linspace(0,np.pi,181),I_emission)
        
        # change I_absorption and I_emission from array to matrix so that we can have dot product.
        I_absorption = np.matrix(I_absorption)
        I_emission = np.matrix(I_emission) 
        
        # I_ex_em = I_ex * et_matrix * I_em.T
        I_absorption_after_et = np.dot(I_absorption, self.et_matrix) 
        self.I_ex_em = np.dot(I_absorption_after_et, I_emission.T)
        self.I_ex_em = self.I_ex_em.T
        
        return
    
    
    
    def compute_M_phase_from_original_2D_portrait(self):    
        '''
        # the way I calculate I0, M_ex, phase_ex, M_em, phase_em is fit with 
        # the equation I = I0 * (1 + M_em * np.cos(2 * (em_angles * np.pi / 180 - phase_em * np.pi / 180)))
    
        I_ex = I0 * (1 + M_ex * np.cos(2 * (ex_angles * np.pi / 180 - phase_ex)))
        I_em = I0 * (1 + M_em * np.cos(2 * (em_angles * np.pi / 180 - phase_em)))
        plt.figure()
        plt.plot(ex_angles, I_ex, 'b', em_angles, I_em, 'r')
        plt.draw()
        '''
        
        # compute M_ex, phase_ex(in r), M_em, phase_em(in r), 
        I0, M_ex, phase_ex, M_em, phase_em = cf.compute_ex_em_modulation_phase (self.I_ex_em)
        
        self.portrait = [I0, M_ex, phase_ex, M_em, phase_em]
        
        return
    
        
    
    def plot_2D_portrait(self):
    
        # plot 2D portrait and ex em curve
        plt.figure(figsize = [17, 4])

        ax1 = plt.subplot(121)
        plt.imshow(self.I_ex_em)
        plt.xlabel('ex')
        plt.ylabel('em')
        plt.gca().invert_yaxis()
        plt.draw()
        # theta_str = str(self.theta).strip('[]')
        # title_str = 'dipoles orientation =' + theta_str + ' (in degree) '
        # plt.title(title_str, fontsize = 14)
        plt.colorbar()

        ax2 = plt.subplot(122)
        ax2.plot(self.ex_angles, np.sum(self.I_ex_em, 0).T, 'b', self.em_angles, np.sum(self.I_ex_em, 1), 'r')
        ax2.set_xlim([0, 180])
        ax2.set_ylim([0, 1.2*np.max(np.sum(self.I_ex_em, 1))])
        plt.xlabel('angles')
        plt.ylabel('intensity')
        
        return    
    
   

    def compute_SFA3(self):
        
        # fit by SFA+3 model
        # these three lines are copied from movie.py, line 142, 143 and 1107
        # according to line 138 and 139, 6 and 4 correspond to the experimental ex and em angles.
        # The angles should be in radian unit
        excitation_angles_grid  = np.linspace(0,np.pi,6, endpoint=False)
        emission_angles_grid    = np.linspace(0,np.pi,4, endpoint=False)
        EX, EM = np.meshgrid(excitation_angles_grid, emission_angles_grid)
        
        M_ex = self.portrait[1]
        phase_ex = self.portrait[2]
                
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
            Ftot = np.append(Ftot, self.I_ex_em[i, column_index]) 
            # print(Ftot)
    
        # normalization. It is according to movie.py, line 1138
        # Note, after normalization, np.sum(Ftotnormed = 1)
        Ftotnormed = Ftot/np.sum(Ftot)
        
        funargs = (EX, EM, M_ex, phase_ex, Ftotnormed)
        
        fac = 1e4 
        pg = 1e-9 
        epsi = 1e-11
        
        fitresult = so.fmin_l_bfgs_b( func=cf.SFA_full_error, \
                                      x0=a0, \
                                          fprime=None, \
                                              args=funargs, \
                                                  approx_grad=True, \
                                                      epsilon=epsi, \
                                                          bounds=list(zip(LB,UB)), \
                                                              factr=fac, \
                                                                  pgtol=pg )
            
        
        self.fitresult = fitresult
        self.Ftot = Ftot
        
        return 


    def plot_SFA3(self):
        
        # plot fitting results: model, Fet, Fnoet. 
        # This is a good way to check fitting property
        
        md_fu = self.fitresult[0][0]
        th_fu = self.fitresult[0][1]
        gr    = self.fitresult[0][2]
        et    = self.fitresult[0][3]
        resi  = self.fitresult[1]
        
        M_ex = self.portrait[1]
        phase_ex = self.portrait[2]
        
        excitation_angles_grid  = np.linspace(0,np.pi,6, endpoint=False)
        emission_angles_grid    = np.linspace(0,np.pi,4, endpoint=False)
        EX, EM = np.meshgrid(excitation_angles_grid, emission_angles_grid)
        
        self.samsum = np.sum(self.Ftot)
        self.Fnoet = cf.SFA_full_func( [md_fu,th_fu,gr,0], EX, EM, M_ex, phase_ex )
        self.Fet   = cf.SFA_full_func( [md_fu,th_fu,gr,1], EX, EM, M_ex, phase_ex )
        self.model = cf.SFA_full_func( [md_fu,th_fu,gr,et], EX, EM, M_ex, phase_ex)
        
        Fnoet_r = self.Fnoet.reshape(np.size(emission_angles_grid),np.size(excitation_angles_grid))
        Fet_r = self.Fet.reshape(np.size(emission_angles_grid),np.size(excitation_angles_grid))
        model_r = self.model.reshape(np.size(emission_angles_grid),np.size(excitation_angles_grid))
        Ftot_r = self.Ftot.reshape(np.size(emission_angles_grid),np.size(excitation_angles_grid))

        
        fig, ax = plt.subplots(1, 4, sharex='all', sharey='all', figsize=(17, 4))
        s_em = range(len(emission_angles_grid))
        
        for n in s_em:
           
            ax[n].plot(excitation_angles_grid, self.samsum*Fet_r[n], 'b>-',  alpha=0.6)
            ax[n].plot(excitation_angles_grid, self.samsum*Fnoet_r[n], 'go-',  alpha=0.6)
            ax[n].plot(excitation_angles_grid, self.samsum*model_r[n], 'rd-',  alpha=0.6)
            ax[n].plot(excitation_angles_grid, Ftot_r[n], 'yp--',  alpha=0.6)
            
            ax[n].set_xlim([0, np.pi])
            ax[n].set_xlabel('ex')
            ax[n].set_title('em'+str(emission_angles_grid[n]*180/np.pi))
            
        
        plt.legend(['Fet', 'Fnoet', 'model', 'Ftot'])
        th_fu_deg = th_fu*180/np.pi
        plt.suptitle( 'md_fu=%f th_fu=%f gr=%f et=%f resi=%f' % (md_fu, th_fu, gr, et, resi))
    
                
        return
       
    
    def reconstruct_Ftot_Fet_Fnoet(self):
    
        md_fu = self.fitresult[0][0]
        th_fu = self.fitresult[0][1]
        gr    = self.fitresult[0][2]
        et    = self.fitresult[0][3]
        
        md_ex = self.portrait[1]
        phase_ex = self.portrait[2]
    
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
        
        fig, (ax1, ax2, ax3) = plt.subplots(figsize = (17, 4), ncols = 3)
        
        h_model = ax1.imshow(np.sum(self.I_ex_em) * modelfine)
        ax1.invert_yaxis()       
        ax1.set_title('model')       
        divider1 = make_axes_locatable(ax1)
        cax1 = divider1.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(h_model, cax = cax1, ax = ax1)
                
        h_Fet = ax2.imshow(np.sum(self.I_ex_em) * Fetfine)
        ax2.invert_yaxis()       
        ax2.set_title('Fet')       
        divider2 = make_axes_locatable(ax2)
        cax2 = divider2.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(h_Fet, cax = cax2, ax = ax2)
        
        h_Fnoet = ax3.imshow(np.sum(self.I_ex_em) * Fnoetfine)
        ax3.invert_yaxis()       
        ax3.set_title('Fnoet')       
        divider3 = make_axes_locatable(ax3)
        cax3 = divider3.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(h_Fnoet, cax = cax3, ax = ax3)
        
        
        
        # plt.figure(figsize=(12, 4))
    
        # plt.subplot(1, 4, 1)
        # plt.imshow(modelfine)
        # plt.gca().invert_yaxis()
        # plt.title('model')
        # plt.colorbar()
    
        # plt.subplot(1, 4, 2)
        # plt.imshow(Fetfine)
        # plt.gca().invert_yaxis()
        # plt.title('Fet')
        # plt.colorbar()

        # plt.subplot(1, 4, 3)
        # plt.imshow(Fnoetfine)
        # plt.gca().invert_yaxis()
        # plt.title('Fnoet' )
        # plt.colorbar()
    
        # plt.subplot(1, 4, 4)
        # plt.text(0.1, 0.5, 'et = %f' % et)
        # plt.axis('off')
        return
    
    
    
    def quick_check_funnel_and_dipoles(self):
        
        # funnel property
        md_fu = self.fitresult[0][0]
        th_fu = self.fitresult[0][1]
        et    = self.fitresult[0][3]
        
        # calculate intensity of each dipole
        et_matrix_dip = np.array(self.et_matrix)
        I_dip = np.sum(et_matrix_dip, 0) / np.size(self.theta)
         
        # bl - baseline
        bl = 0
        
              
        plt.figure(figsize = (17, 4))
        # plot baseline
        plt.plot([0, 180], [bl, bl], 'k', linewidth = 7)
        plt.xlim(-2, 182)
        plt.ylim(-0.2, 1.2)

        # plot dipoles
        n_dip = range(len(self.theta))
        for n in n_dip: 
                plt.plot((self.theta[n], self.theta[n]), (bl, I_dip[n]), 'k', linewidth = 7)
                plt.text(self.theta[n], I_dip[n] + 0.2, ' md_dip=%0.3f \n th_dip=%0.3f \n I=%0.3f ' % (1, self.theta[n], I_dip[n]), fontsize = 12)
    
 
        # plot funnel
        th_fu_deg = th_fu * 180 / np.pi
        plt.plot((th_fu_deg, th_fu_deg), (bl, et), 'r', alpha = 1, linewidth = 4)
        plt.text(th_fu_deg, et, ' md_fu=%0.3f \n th_fu=%0.3f \n et=%0.3f ' % (md_fu, th_fu_deg, et), fontsize = 12)

        
        
    




    


































    

    
    