# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 20:11:46 2020

@author: sjz
"""

# et - r0(anisotropy) - beta(angle between dipoles)

import numpy as np
import matplotlib.pyplot as plt

beta_deg = np.linspace(0, 180, 11)
beta_r = beta_deg * np.pi / 180

r0 = 0.2 * (3 * np.cos(beta_r) **2 - 1)
et = (2 - 5 * r0)/(2 + r0)

# et [et >= 1] = 1

plt.figure()
plt.plot(beta_deg, et, 'ro--')
plt.plot(beta_deg, r0, 'yo--')
plt.xlabel('beta in degree')
plt.legend(['et', 'r0'])

plt.figure()
plt.plot(et, r0, 'ko--')
plt.xlabel('et')
plt.ylabel('r0')


plt.legend(['simulation', 'analytical solution'])