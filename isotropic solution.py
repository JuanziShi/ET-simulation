# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 16:34:58 2020

@author: Juanzi
"""

import numpy as np
import matplotlib.pyplot as plt
import addcopyfighandler

plt.rcParams.update({'font.size': 15})

plt.close('all')

phi = np.linspace(0, 2*np.pi, 50)
epsilon = np.linspace(0, 1, 11)

I_et = 1
M_et = 0 # et is flat
theta_et =  0 * np.pi/180 

I_noet = 1
M_noet = 0.5
theta_noet =  0 * np.pi/180 

I1 = I_et * (M_et * np.cos(2 * (phi - theta_et)) + 1)
I2 = I_noet * (M_noet * np.cos(2 * (phi - theta_noet)) + 1)


s = 0
Mf = np.zeros((11,1))
anisotropy = np.zeros((11,1))
for n in epsilon:
    If = n * I1 + (1 - n) * I2
    
    Mf[s][0] = (np.max(If) - np.min(If))/(np.max(If) + np.min(If))
    anisotropy[s][0] = (np.max(If) - np.min(If))/(np.max(If) + 2 * np.min(If))
    
    s = s + 1 

    plt.figure()
    plt.plot(phi * 180/np.pi, I1, 'b')
    plt.plot(phi * 180/np.pi, I2, 'g')
    plt.plot(phi * 180/np.pi, If, 'r--')

    plt.legend(['et', 'noet', 'model'])
    plt.title('epsilon = %f' % (n))
    
plt.figure()
plt.plot(epsilon, Mf, 'ko-')
plt.ylabel('Modulation depth')
plt.xlabel('\u03B5') # epsilon

plt.figure()
plt.plot(epsilon, anisotropy,'ko-')
plt.ylabel('Anisotropy')
plt.xlabel('\u03B5') # epsilon