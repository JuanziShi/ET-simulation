# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 16:46:36 2020

@author: sjz
"""

import numpy as np
import matplotlib.pyplot as plt


theta = np.array([0, 30, 60])

et_matrix = np.array([[0.4, 0.3, 0.3],
                      [0, 1, 0],
                      [0, 0, 1]])


I = np.sum(et_matrix,0)/np.size(theta)

dip_n = range(len(theta))

# bl - baseline
bl = 0

fig = plt.figure(figsize = (17, 4))

# plot baseline
plt.plot([0, 180], [bl, bl], 'k')
plt.xlim(-2, 182)
plt.ylim(-0.2, 1)

# plot funnel
plt.plot((75, 75), (0, 0.5), 'r')
plt.text(75, 0.5, ' md_fu=%0.2f \n th_fu=%0.2f \n et=%0.2f ' % (0.8, 75, 0.5))


# plot dipoles
for n in dip_n: 
        plt.plot((theta[n], theta[n]),(bl, I[n]), 'k')
        
        








