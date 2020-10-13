# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 09:20:55 2020

@author: Juanzi
"""



gr = P.fitresult[0][2]
alpha = P.fitresult[0][4]

Imax = gr+2*(np.cos(alpha)**2)
Imin = 2*(np.sin(alpha)**2)

Mex_3d = (Imax - Imin)/(Imax + Imin)
Mex = P.portrait[1]

print ('Mex_3d = %f' % (Mex_3d))
print ('Mex = %f' % (Mex))
print (Mex-Mex_3d)


gr = P.fitresult[0][2]
alpha = P.fitresult[0][4]
beta = P.fitresult[0][5]

Imax = gr+np.cos(alpha)**2 + np.cos(beta)**2
Imin = np.sin(alpha)**2 + np.sin(beta)**2

Mex_3d = (Imax - Imin)/(Imax + Imin)
Mex = P.portrait[1]

print ('Mex_3d = %f' % (Mex_3d))
print ('Mex = %f' % (Mex))
print (Mex-Mex_3d)
