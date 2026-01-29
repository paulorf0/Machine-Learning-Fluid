import numpy as np

'''
    dir : np.array([x : float, y : float]) # difference between the position of particles
    r : float # Distance between particles
    h : float # Its height of cell
'''


def Spiky_Gradient(diff_pos, r, h):
    if r <= 0 or r > h:
        return np.array([0.0, 0.0])
    
    term = -30 / (np.pi * h ** 5)
    
    return term * (h-r)**2 * (diff_pos/r)
