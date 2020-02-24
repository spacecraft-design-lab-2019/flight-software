# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 19:36:55 2019

@author: Paul DeTrempe

@description: Implementation of magnetorquer detumbling laws (See Wertz 7.5)
"""
import math
import ulab as np

# def detumble_B_cross(omega,B,k):
#     '''
#     Takes in the angular rate and magnetic field vectors (in principal frame)
#     (as 3x1 np arrays) and returns a 3x1 vector of control torque to detumble.
    
#     - based on the paper by AVANZINI AND GIULIETTI
#     TODO: find optimal k for our system
#     '''
#     # try adjusting k to the velocity
#     # k = -2*omega
#     b = B/np.linalg.norm(B) # normalize magnetic field vector
#     L = -k* (np.identity(3) - b @ np.transpose(b)) @ omega
#     return L
    
def detumble_B_dot(B,B_dot,k=1):
    '''
    Takes in magnetic field, magnetic field rate (as 3x1 vectors, in principal frame), and control gain (scalar)
    and returns a 3x1 control moment
    
    TODO: find optimal k for our system
    '''
    Bt = B.copy()
    Bt.transpose()
    m = B_dot / (math.sqrt(np.dot(B, Bt)[0])/k)
    # B_norm = math.sqrt(sum(x*x for x in B))
    # m = [k*x/B_norm for x in B_dot]
    return m

# def detumble_B_dot_bang_bang(B_dot, max_dipoles = [[8.8e-3],[1.373e-2],[8.2e-3]]):
#     '''
#     :param B_dot: 3x1 vector of the rate of change of Earth's magnetic field, [nanoTesla/s], as measured in the spacecraft body
#                     frame.
#     :param max_dipoles: 3x1 vector of max dipole values [Amp-m^2] in the x, y, and z body (principal) axis directions.
#     :return: m, a 3x1 vector of the dipole commanded by the bang-bang b_dot control law.
#     references: Wertz, equation (7.54)

#     '''
#     m = np.zeros((3,1))
#     m[0] = max_dipoles[0] * -np.sign(np.dot(np.transpose(np.array([[1.0],[0.0],[0.0]])) , np.transpose(B_dot)))
#     m[1] = max_dipoles[1] * -np.sign(np.dot(np.transpose(np.array([[0.0],[1.0],[0.0]])) , np.transpose(B_dot)))
#     m[2] = max_dipoles[2] * -np.sign(np.dot(np.transpose(np.array([[0.0],[0.0],[1.0]])) , np.transpose(B_dot)))
#     return m
    
def get_B_dot(B1,B2,dt):
    '''
    Takes in two magnetic field measurements (3x1) and the timestep between them and returns
    a first order approximation to the rate of change of the magnetic field (3x1)
    '''
    B_dot = (B2-B1)/dt
    # B_dot = [(b-a)/dt for a, b in zip(B1, B2)]
    return B_dot
    