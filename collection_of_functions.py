# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
# import matplotlib.pyplot as plt

def get_ex_electric_field():
    
    ex_angles_r  = np.linspace( 0, np.pi, 181 )
    
    # field vector is rotated on the yz plane. In the array (x, y, z)
    ex_ori = np.zeros((ex_angles_r.size, 3))
    
    # spherical coordinates, r is equal to 1
    # azimuthal angle is always 90 degree, becasue we calculate the projection on yz plane.
    phi = np.ones(ex_angles_r.size)*np.pi/2 
    theta = ex_angles_r
    
    # from spherical coordinates to cartersian coordinate. 
    # equation from Rafael's thesis, page 18, eq 13
    ex_ori[:,0] = np.cos(phi)*np.sin(theta) # x
    ex_ori[:,1] = np.sin(phi)*np.sin(theta) # y
    ex_ori[:,2] = np.cos(theta)             # z
    
    # to remove the numerical noise
    ex_ori[:,0] = ex_ori[:,0]*0 
    
    # plot the excitation E field 
    # plt.scatter( ex_ori[:,1], ex_ori[:,2])
      
    return ex_ori


def get_em_polarizer():
    
    em_angles_r = np.linspace(0, np.pi, 181)
    
    #field vector is rotated on the yz plane. In the array (x, y, z)
    em_ori = np.zeros((em_angles_r.size, 3))
    
    # spherical coordinate, r is equal to 1
    # azimuthal angle is always 90 degree, because we calculate the projection on yz plane
    phi = np.ones(em_angles_r.size)*np.pi/2
    theta = em_angles_r
    
    # from spherical coordinates to cartersian coordinate
    # equation from Rafael's thesis, page 18, eq 13
    em_ori[:,0] = np.cos(phi)*np.sin(theta) # x
    em_ori[:,1] = np.sin(phi)*np.sin(theta) # y
    em_ori[:,2] = np.cos(theta)             # z
    
    # to remove numerical noise
    em_ori[:,0] = em_ori[:,0]*0 
    
    # plot the excitation E field 
    # plt.scatter( em_ori[:,1], em_ori[:,2])
    
    return em_ori
    










