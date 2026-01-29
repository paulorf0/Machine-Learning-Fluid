'''
    r : float # Distance between particles
    h : float # Its height of cell
'''

import numpy as np

def Poly6(r, h):
    term = 4 / (np.pi * h ** 8)
    return term * (h**2 - r**2)**3