# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:47:01 2020

@author: sjz
"""

import numpy as np
import matplotlib.pyplot as plt
import addcopyfighandler

phi = np.linspace(0, 2*np.pi, 50)

I_1 = 0.4
M_1 = 1
theta_1 =  0 * np.pi/180 

I_2 = 0.3
M_2 = 1
theta_2 = 36 * np.pi/180 

I_3 = 0.3
M_3 = 1
theta_3 = 72 * np.pi/180 

I_f = 1
M_f = 0.52
theta_f = 30.78 * np.pi/180 

I1 = I_1 * (M_1 * np.cos(2*(phi-theta_1))+1)
I2 = I_2 * (M_2 * np.cos(2*(phi-theta_2))+1)
I3 = I_3 * (M_3 * np.cos(2*(phi-theta_3))+1)
If = I_f * (M_f * np.cos(2*(phi-theta_f))+1)

plt.rcParams.update({'font.size': 18})
plt.figure()
plt.plot(phi * 180/np.pi, I1, 'b')
plt.plot(phi * 180/np.pi, I2, 'g')
plt.plot(phi * 180/np.pi, I3, 'm')
plt.plot(phi * 180/np.pi, If, 'r')
plt.plot(phi * 180/np.pi, I1+I2+I3, 'yp--')

plt.legend(['emitter1', 'emitter2', 'emitter3', 'single funnel', 'emitter1 + emitter2 + emitter3'])