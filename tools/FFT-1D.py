# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 20:43:24 2020

@author: sjz
"""

import numpy as np

# Number of sample points
N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(90.0 * 2.0*np.pi*x)
yf = np.fft.fft(y)
xf = np.fft.fftfreq(N, T) # xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

import matplotlib.pyplot as plt
plt.figure()
plt.plot(xf[0:N//2], 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.show()

plt.figure()
plt.plot(xf, 2.0/N * np.abs(yf))
